import mlflow
from mlflow.pyfunc import PyFuncModel
from typing import Optional

mlflow.set_tracking_uri("http://127.0.0.1:5000")

MODEL_NAME = "a2-demo-model"

def load_model_from_registry(version: Optional[str] = None) -> tuple[PyFuncModel, str]:
    if version is None:
        uri = f"models:/{MODEL_NAME}/latest"
    else:
        uri = f"models:/{MODEL_NAME}/{version}"

    model = mlflow.pyfunc.load_model(uri)
    return model, uri
