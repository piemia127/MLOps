import joblib
import numpy as np

# load model.pkl（including w, b, mu, sigma）
_bundle = joblib.load("model.pkl")
_w = np.asarray(_bundle["w"], dtype=float)
_b = float(_bundle["b"])
_mu = np.asarray(_bundle["mu"], dtype=float)
_sigma = np.asarray(_bundle["sigma"], dtype=float)

def predict(features: list[float]) -> float:
    """
    LASSO Regression: y = ( (x - mu) / sigma ) · w + b
    """
    x = np.asarray(features, dtype=float)
    x_norm = (x - _mu) / _sigma
    y = float(np.dot(x_norm, _w) + _b)
    return y
