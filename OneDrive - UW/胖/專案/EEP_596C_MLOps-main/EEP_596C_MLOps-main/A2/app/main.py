import numpy as np
import mlflow
from fastapi import FastAPI, Query
from datetime import datetime, timezone
from typing import Optional
from app.schemas import InputData, PredictResponse, Metadata
from app.registry import load_model_from_registry

APP_VERSION = "0.1.0"  # App ver.

app = FastAPI(
    title="MLOps A2 Model Serving",
    version=APP_VERSION,
)

@app.post("/predict", response_model=PredictResponse)
def predict_api(data: InputData, model_version: Optional[str] = None):
    features = [
        data.crim,
        data.zn,
        data.indus,
        data.chas,
        data.nox,
        data.rm,
        data.age,
        data.dis,
        data.rad,
        data.tax,
        data.ptratio,
        data.b,
        data.lstat
    ]

    timestamp_utc = datetime.now(timezone.utc).isoformat()

    model_version_uri = f"models:/a2-demo-model/{model_version or 'latest'}"
    model = mlflow.pyfunc.load_model(model_version_uri)
    prediction = float(model.predict(np.array([features]))[0])

    return {
        "prediction": prediction,
        "metadata": {
            "app_version": APP_VERSION,
            "model_version": model_version_uri,
            "timestamp_utc": timestamp_utc
        }
    }
