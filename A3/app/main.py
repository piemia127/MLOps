import numpy as np
import mlflow
from fastapi import FastAPI
from datetime import datetime, timezone
from typing import Optional
from app.schemas import InputData, PredictResponse
from app.registry import load_model_from_registry

# === Prometheus & OpenTelemetry Imports ===
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

APP_VERSION = "0.2.0"

app = FastAPI(
    title="MLOps A3 Model Serving with Metrics and Tracing",
    version=APP_VERSION,
)

# Prometheus Metric
prediction_metric = Gauge(
    "model_prediction_value",
    "Predicted value from MLflow model"
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
)

instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)

# OpenTelemetry Tracing
resource = Resource.create({
    SERVICE_NAME: "fastapi-mlops-a3",
})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://localhost:14268/api/traces",
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
tracer = trace.get_tracer(__name__)

# Predict Endpoint
@app.post("/predict", response_model=PredictResponse)
def predict_api(data: InputData, model_version: Optional[str] = None):
    features = [
        data.crim, data.zn, data.indus, data.chas, data.nox,
        data.rm, data.age, data.dis, data.rad, data.tax,
        data.ptratio, data.b, data.lstat
    ]

    timestamp_utc = datetime.now(timezone.utc).isoformat()

    model_version_uri = f"models:/a2-demo-model/{model_version or 'latest'}"
    model = mlflow.pyfunc.load_model(model_version_uri)
    prediction = float(model.predict(np.array([features]))[0])

    # Record Prometheus Metric
    prediction_metric.set(prediction)

    # Record OpenTelemetry Trace
    with tracer.start_as_current_span("model_prediction") as span:
        span.set_attribute("model.version", model_version or "latest")
        span.set_attribute("prediction.value", prediction)
        span.set_attribute("timestamp.utc", timestamp_utc)
        span.set_attribute("request.features.count", len(features))
        span.set_attribute("request.input.summary", str(features[:3]) + " ...")
        span.set_attribute("service.app_version", APP_VERSION)

    return {
        "prediction": prediction,
        "metadata": {
            "app_version": APP_VERSION,
            "model_version": model_version_uri,
            "timestamp_utc": timestamp_utc
        }
    }
