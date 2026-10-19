# Architecture and scope

## Logical flow

1. **Ingestion:** the academic project imported a CSV dataset into `TRAFFIC_PROJECT.RAW.TRAFFIC_DATA` in Snowflake.
2. **Analytical preparation:** `TRAFFIC_PROJECT.ANALYTICS.TRAFFIC_CLEAN` was built and dimension tables were used to represent weather, driver experience and road quality.
3. **Dimensional model:** `FACT_TRAFFIC`, `DIM_WEATHER`, `DIM_DRIVER`, `DIM_ROAD_QUALITY` supported analytical queries and model training.
4. **ML preparation:** a fitted scikit-learn preprocessor, provided within the group project, was stored on a Snowflake stage.
5. **Training:** a Snowflake notebook used Snowpark, pandas and scikit-learn to train and compare Linear Regression, Random Forest and Gradient Boosting.
6. **Serving:** Streamlit in Snowflake downloads the fitted preprocessor and serialized model from the stage, takes user inputs and predicts `stress_index`.

## Responsibility boundaries

| Component | Visible in this repository? | Notes |
| --- | --- | --- |
| Raw dataset / ingestion scripts | No | Licensing and complete ingestion code not supplied |
| DWH SQL / EDA | Architectural description only | Part of the wider academic group work |
| Model training and comparison | Yes | Exported notebook, without outputs |
| Fitted scikit-learn preprocessor | No | Snowflake stage artifact; ownership/permissions not verified |
| Trained ML model binary | No | Requires access to the target Snowflake stage |
| Streamlit application | Yes | Adapted to notebook feature schema; requires verification in Snowflake |
| Full diploma thesis | No | Group work; publication approvals not yet established |

## Runtime integration

- Snowpark's `get_active_session()` is provided inside Snowflake.
- `session.sql(...).to_pandas()` retrieves database values for the app's slider limits.
- `session.file.get(...)` downloads the trusted `.pkl` files from the Snowflake stage.
- `joblib.load()` deserializes artifacts; loading untrusted files is unsafe.
- The selected model is applied to the transformed **six-feature** input record.

## Limitations

The repository is an **architecture and portfolio demonstration**, not an independently runnable end-to-end solution. It does not provision Snowflake resources, create the dataset, train the preprocessing pipeline or provide a public deployment. The fitted preprocessing pipeline may have been constructed prior to the train/test split; its fitting methodology cannot be verified from this repository alone, so reported evaluation should be treated as academic rather than production validation.
