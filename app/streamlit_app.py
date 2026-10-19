"""Traffic Stress Index predictor for Streamlit in Snowflake.

Portfolio adaptation of the supplied app, aligned with the supplied ML notebook:
model inputs are the six features used during training. The derived congestion
index is displayed for context only, NOT passed to the model.

Runtime requires an active Snowflake session, a populated analytics table,
and trusted joblib artifacts on a Snowflake stage.
"""

import os
import joblib
import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session

STAGE_NAME = "@ML_ARTIFACTS_DB.PREPROCESSING.MODEL_ARTIFACTS"
PREPROCESSOR_FILENAME = "preprocessor_20260514_202212.pkl"
MODEL_FILENAME = "traffic_stress_best_model.pkl"
SOURCE_TABLE = "TRAFFIC_PROJECT.ANALYTICS.FACT_TRAFFIC"

# Must match feature_columns in notebooks/model_training_snowflake.ipynb.
MODEL_FEATURES = [
    "horn_events_per_min", "avg_speed", "road_quality_score",
    "traffic_density", "weather_condition", "driver_experience_level"
]

st.set_page_config(page_title="Predykcja stresu kierowcy", layout="centered")
st.title("Predykcja wskaźnika stresu kierowcy")
st.write(
    "Model przewiduje wartość `stress_index` na podstawie parametrów ruchu, "
    "warunków pogodowych, jakości drogi i doświadczenia kierowcy. "
    "To demonstracja edukacyjna, a nie pomiar medyczny."
)

try:
    session = get_active_session()
except Exception as exc:
    st.error("Aplikacja wymaga uruchomienia w środowisku Streamlit in Snowflake.")
    st.exception(exc)
    st.stop()


def find_file(folder, filename):
    for root, _, files in os.walk(folder):
        if filename in files:
            return os.path.join(root, filename)
    return None


@st.cache_resource
def load_artifacts():
    local_dir = "/tmp/model_artifacts"
    os.makedirs(local_dir, exist_ok=True)
    for filename in (PREPROCESSOR_FILENAME, MODEL_FILENAME):
        session.file.get(f"{STAGE_NAME}/{filename}", local_dir)
    preprocessor_path = find_file(local_dir, PREPROCESSOR_FILENAME)
    model_path = find_file(local_dir, MODEL_FILENAME)
    if not preprocessor_path or not model_path:
        raise FileNotFoundError("Nie znaleziono wymaganych artefaktów na Snowflake Stage.")
    # Only load pickle/joblib files from a stage that you own and trust.
    return joblib.load(preprocessor_path), joblib.load(model_path)


@st.cache_data
def get_numeric_ranges():
    query = f"""
    SELECT
      MIN(traffic_density) AS min_traffic_density,
      MAX(traffic_density) AS max_traffic_density,
      MIN(horn_events_per_min) AS min_horn_events_per_min,
      MAX(horn_events_per_min) AS max_horn_events_per_min,
      MIN(avg_speed) AS min_avg_speed,
      MAX(avg_speed) AS max_avg_speed,
      MIN(signal_wait_time) AS min_signal_wait_time,
      MAX(signal_wait_time) AS max_signal_wait_time
    FROM {SOURCE_TABLE}
    """
    result = session.sql(query).to_pandas()
    result.columns = [col.lower() for col in result.columns]
    if result.empty or result.iloc[0].isnull().any():
        raise ValueError("Brak odpowiednich danych do ustalenia zakresów suwaków.")
    return result.iloc[0]


try:
    preprocessor, model = load_artifacts()
    ranges = get_numeric_ranges()
except Exception as exc:
    st.error("Nie udało się wczytać modelu, preprocessora lub danych z Snowflake.")
    st.exception(exc)
    st.stop()


def default_value(lower, upper, proposed):
    return max(lower, min(upper, proposed))


def numeric_slider(label, column, proposed, step):
    low = float(ranges[f"min_{column}"])
    high = float(ranges[f"max_{column}"])
    return st.sidebar.slider(label, min_value=low, max_value=high,
                             value=default_value(low, high, proposed), step=step)


st.sidebar.header("Parametry jazdy")
traffic_density = numeric_slider("Traffic density", "traffic_density", 80.0, 1.0)
horn_events_per_min = numeric_slider("Horn events per minute", "horn_events_per_min", 8.0, 0.1)
avg_speed = numeric_slider("Average speed", "avg_speed", 40.0, 0.1)
signal_wait_time = numeric_slider("Signal wait time", "signal_wait_time", 40.0, 0.1)
weather_condition = st.sidebar.selectbox("Weather condition", ["Clear", "Foggy", "Hot", "Rainy"])
road_quality_score = st.sidebar.slider("Road quality score", 1, 10, 6, 1)
driver_experience_level = st.sidebar.selectbox(
    "Driver experience level", ["Beginner", "Intermediate", "Expert"]
)

# Historical UI metric; not one of the six features in the training notebook.
congestion_index = traffic_density * signal_wait_time

model_input = pd.DataFrame([{
    "horn_events_per_min": horn_events_per_min,
    "avg_speed": avg_speed,
    "road_quality_score": road_quality_score,
    "traffic_density": traffic_density,
    "weather_condition": weather_condition,
    "driver_experience_level": driver_experience_level,
}], columns=MODEL_FEATURES)

st.subheader("Dane wejściowe")
display_data = {
    "traffic_density": traffic_density,
    "horn_events_per_min": horn_events_per_min,
    "avg_speed": avg_speed,
    "signal_wait_time": signal_wait_time,
    "congestion_index (informacyjnie)": congestion_index,
    "weather_condition": weather_condition,
    "road_quality_score": road_quality_score,
    "driver_experience_level": driver_experience_level,
}
st.dataframe(pd.DataFrame({"Parametr": list(display_data), "Wartość": list(display_data.values())}),
             use_container_width=True, hide_index=True)

if st.button("Przewidź stress_index"):
    try:
        processed = preprocessor.transform(model_input)
        predicted_stress = float(model.predict(processed)[0])
        st.subheader("Wynik predykcji")
        st.metric("Przewidywany stress_index", round(predicted_stress, 2))
        if predicted_stress < 35:
            st.success("Interpretacja: niski poziom indeksu stresu kierowcy.")
        elif predicted_stress < 65:
            st.warning("Interpretacja: średni poziom indeksu stresu kierowcy.")
        else:
            st.error("Interpretacja: wysoki poziom indeksu stresu kierowcy.")
    except Exception as exc:
        st.error("Nie udało się wykonać predykcji. Sprawdź zgodność modelu i preprocessora.")
        st.exception(exc)

with st.expander("Jak działa ta aplikacja?"):
    st.markdown(
        "Aplikacja pobiera dane z formularza i przekazuje **sześć cech** do preprocessora "
        "oraz modelu wytrenowanego w notebooku. "
        "`signal_wait_time` i wyliczony `congestion_index` są wyświetlane informacyjnie; "
        "nie są wejściem modelu udokumentowanego w notebooku. "
        "Preprocessor skaluje wartości numeryczne i koduje kategorie. "
        "Model zwraca prognozowaną wartość `stress_index`."
    )

with st.expander("Informacja techniczna"):
    st.write("Wymagane pliki na Snowflake Stage:")
    st.code(f"{STAGE_NAME}/{PREPROCESSOR_FILENAME}\n{STAGE_NAME}/{MODEL_FILENAME}")
    st.write(f"Zakresy suwaków są wyznaczane na podstawie `{SOURCE_TABLE}`.")
    st.info("Wersja portfolio — kod dopasowany do notebooku; niezweryfikowany na aktywnym koncie Snowflake.")
