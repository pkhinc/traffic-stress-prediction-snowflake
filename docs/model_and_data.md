# Model, data and evaluation

## Dataset

The submitted academic report describes **50,000 observations** with a target `stress_index` in the **0–100** range. Source dataset provenance and redistribution rights were not documented sufficiently in the available publishable materials; **the data is not included**. Do not represent the records as live traffic or clinically measured stress without independent verification.

## Data model

A Snowflake database, `TRAFFIC_PROJECT`, is described with two schemas:

- `RAW`: imported source table `TRAFFIC_DATA`.
- `ANALYTICS`: cleaned data and star-schema-inspired tables `FACT_TRAFFIC`, `DIM_WEATHER`, `DIM_DRIVER`, `DIM_ROAD_QUALITY`.

The SQL definitions and initial EDA belong to the broader group-work scope; their source files were not provided for this public repository.

## Inference contract: notebook-aligned version

| Input feature | Type | Role |
| --- | --- | --- |
| `horn_events_per_min` | Numeric | Model input |
| `avg_speed` | Numeric | Model input |
| `road_quality_score` | Numeric | Model input |
| `traffic_density` | Numeric | Model input |
| `weather_condition` | Categorical | Model input |
| `driver_experience_level` | Ordered categorical | Model input |
| `signal_wait_time` | Numeric | UI-only explanatory field |
| `congestion_index` | Derived numeric | UI-only explanatory field |

The preprocessor described in the academic work scales numeric inputs, applies one-hot encoding to weather and ordinal encoding to experience; it returns eight transformed features. Exact runtime compatibility with the stage binary must still be tested.

## Evaluation

Models: Linear Regression, Random Forest Regressor, Gradient Boosting Regressor. In the original notebook, an 80/20 split and `random_state=42` were used, with evaluation via MAE, RMSE and R². The model with the lowest test RMSE was written to the Snowflake stage.

| Model | MAE (test) | RMSE (test) | R² (test) |
|---|---:|---:|---:|
| Linear Regression | 4.2088 | 5.2746 | 0.8946 |
| Random Forest Regressor | 4.0554 | 5.0699 | 0.9026 |
| Gradient Boosting Regressor | 3.9449 | 4.9338 | 0.9078 |

*Source: numeric results recorded in the submitted academic thesis. No fresh training or metrics recomputation has been performed for this repository.*

## Known historical mismatch and portfolio adaptation

The **original supplied Streamlit source** passed `congestion_index` and omitted `traffic_density`, while the **model training notebook** does the opposite. The original Streamlit code also expected a model binary named `gradient_boosting_model.pkl`, while the notebook saves `traffic_stress_best_model.pkl`. Earlier textual descriptions mentioned an older preprocessor date than the file loaded by the Python code.

The copy in `app/streamlit_app.py` uses the notebook's six model features, `preprocessor_20260514_202212.pkl` and `traffic_stress_best_model.pkl`. This is a **proposed integration alignment**, not evidence that the modified UI was successfully run in Snowflake. Screenshots show the earlier version.

## Reproducibility limits

- Data and fitted `.pkl` files are not included.
- Versions of Python and scikit-learn used during original serialization must be compatible with the runtime.
- The process used to *fit* the preprocessor is not in the supplied model-training notebook; verifying absence of preprocessing leakage requires the earlier pipeline code.
- Prediction depends on the model and preprocessor having been trained and saved together against the same feature contract.
