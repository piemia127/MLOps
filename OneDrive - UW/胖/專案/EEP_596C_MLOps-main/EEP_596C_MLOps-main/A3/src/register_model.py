import joblib
import numpy as np
import mlflow
from mlflow.pyfunc import PythonModel
from mlflow.models import infer_signature

mlflow.set_tracking_uri("http://127.0.0.1:5000")

MODEL_NAME = "a3-demo-model"

bundle = joblib.load("../model.pkl")

_w = np.asarray(bundle["w"], dtype=float)
_b = float(bundle["b"])
_mu = np.asarray(bundle["mu"], dtype=float)
_sigma = np.asarray(bundle["sigma"], dtype=float)


class BostonLassoWrapper(PythonModel):
    def predict(self, context, model_input):
        # model_input = 2D array of shape (n, 13)
        x = (model_input - _mu) / _sigma
        y = np.dot(x, _w) + _b
        return y


def main():
    example = np.array([[0.1, 0.0, 10.0, 0.0, 0.5, 6.0, 65.0, 3.5, 5.0, 293.0, 16.0, 390.0, 10.0]])

    signature = infer_signature(example, np.array([0.0]))

    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=BostonLassoWrapper(),
            registered_model_name=MODEL_NAME,
            input_example=example,
            signature=signature
        )
        print("Boston Housing model has registered as new Model Registry version")


if __name__ == "__main__":
    main()
