from fastapi import FastAPI
from app.model import predict
from app.schemas import InputData, PredictResponse

app = FastAPI()

@app.post("/predict", response_model=PredictResponse)
def predict_api(data: InputData):
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
    result = predict(features)
    return {"prediction": result}
