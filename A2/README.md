# A2: Serve Versioned ML Model via MLflow Model Registry + FastAPI

## Summary
This project upgrades **A1’s FastAPI model serving** by integrating **MLflow Model Registry**, enabling versioned model management and dynamic model selection at inference time.  
The FastAPI server now supports:
- Selecting a specific model version (`/predict?model_version=2`)
- Automatically using the **latest** version if not provided
- Returning **metadata** (app version, model version, timestamp)


## What This Project Includes

- **MLflow Model Registry** (local tracking server and artifact store)
- **Versioned model registration** (`a2-demo-model`, ver. `1`, `2`, …)
- **FastAPI endpoint using MLflow model URI**
- **Pydantic input validation** for safety
- **Basic pytest tests** (`happy path + invalid input`)
- **Model + App version included in API output**

**Example FastAPI URL:**  
`http://127.0.0.1:8000/docs`

**Example Request**

`
curl -X 'POST' 'http://127.0.0.1:8000/predict?model_version=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "crim": 0.1,
  "zn": 0.0,
  "indus": 10.0,
  "chas": 0,
  "nox": 0.5,
  "rm": 6.0,
  "age": 65.0,
  "dis": 3.5,
  "rad": 5,
  "tax": 293,
  "ptratio": 16.0,
  "b": 390.0,
  "lstat": 10.0
}'
`

**Example Response**

`
{
  "prediction": 19.123,
  "metadata": {
    "app_version": "0.1.0",
    "model_version": "models:/a2-demo-model/2",
    "timestamp_utc": "2025-10-29T05:13:00Z"
  }
}
`

## Reflections
### What Was Easy
MLflow model registration using mlflow.pyfunc.log_model

Adding FastAPI query parameter to dynamically pick model version

### What Was Hard
Debugging MLflow input shape enforcement

Ensuring FastAPI + pytest recognized the app module path correctly


## Resources Used
- MLflow official docs — Model Registry & pyfunc serving
- pytest official docs
- Assignment guide
- ChatGPT for debugging MLflow + FastAPI integration