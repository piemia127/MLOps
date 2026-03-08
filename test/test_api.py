import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_happy_path():
    payload = {
        "crim": 0.1,
        "zn": 0.0,
        "indus": 10.0,
        "chas": 0,
        "nox": 0.5,
        "rm": 6.0,
        "age": 65.0,
        "dis": 3.5,
        "rad": 5,
        "tax": 293.0,
        "ptratio": 16.0,
        "b": 390.0,
        "lstat": 10.0
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "metadata" in data
    assert data["metadata"]["app_version"] == "0.1.0"

def test_predict_invalid_input_age_negative():
    payload = {
        "crim": 0.1,
        "zn": 0.0,
        "indus": 10.0,
        "chas": 0,
        "nox": 0.5,
        "rm": 6.0,
        "age": -5.0,  # invalid
        "dis": 3.5,
        "rad": 5,
        "tax": 293.0,
        "ptratio": 16.0,
        "b": 390.0,
        "lstat": 10.0
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # FastAPI should reject it
