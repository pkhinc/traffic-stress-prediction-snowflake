# Deployment: Streamlit in Snowflake

## Prerequisites

- A Snowflake account with permission to use Streamlit in Snowflake.
- The analytic table `TRAFFIC_PROJECT.ANALYTICS.FACT_TRAFFIC` with the columns queried by `app/streamlit_app.py`.
- The required dimension tables for rerunning `notebooks/model_training_snowflake.ipynb`.
- Access to the Snowflake stage `@ML_ARTIFACTS_DB.PREPROCESSING.MODEL_ARTIFACTS` containing:
  - `preprocessor_20260514_202212.pkl`
  - `traffic_stress_best_model.pkl`
- Compatible package versions for Python, Streamlit, pandas, scikit-learn, joblib and Snowpark. See `config/environment.yml` and `config/pyproject.toml` (they represent different dependency configuration mechanisms; follow the UI of the chosen Snowflake runtime).

> **Important:** these `.pkl` files were **not supplied** for this portfolio package. The second name is the output of the submitted model-training notebook; verify that the real stage contains that output. Do not rename some other model and assume compatibility.

## Publishing inside Snowflake

1. In Snowflake, confirm that the database, table, stage and both model files exist and that the app's execution role can read them.
2. Create or edit a Streamlit in Snowflake application under an authorized warehouse/runtime.
3. Use `app/streamlit_app.py` as its entry point (copy the source according to Snowflake's editor/file upload workflow).
4. Configure the required libraries in the environment/package settings, using the supplied configuration as a reference.
5. If your own Snowflake object names differ, update `STAGE_NAME` and `SOURCE_TABLE` in the app and relevant notebook SQL.
6. Run the app in Snowflake. Verify the app loads its preprocessor and model, and that changes in model input variables produce predictions.
7. Inspect errors and confirm the model's six features exactly match the notebook and fitted preprocessor. Compare predicted values with a controlled test record before advertising the deployment as working.

## Why `streamlit run app/streamlit_app.py` is not enough

The app calls `get_active_session()`, which relies on a Snowflake-managed execution environment. Merely installing Python packages locally does not create that active session, the analytic Snowflake table or the saved model artifacts. A standalone version would need a separate, intentionally designed local data/model-loading path.

## Security and costs

- Never commit Snowflake passwords, private keys, tokens, session dumps or `.streamlit/secrets.toml`.
- `joblib.load()` can execute unsafe content: load only artifacts you created or obtained from a trusted internal stage.
- Keep cloud object privileges limited to what the app requires; a publicly visible GitHub repository **does not** grant Snowflake permissions.
- A Streamlit in Snowflake deployment may incur charges depending on Snowflake account configuration and usage. Confirm current billing before enabling or sharing it.
