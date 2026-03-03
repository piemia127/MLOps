# A3: Observability Instrumentation (Prometheus + Jaeger + OpenTelemetry)

## Summary
This project extends A2’s MLflow + FastAPI model serving system by adding observability and distributed tracing.
Through Prometheus, Grafana, and Jaeger (OpenTelemetry) integration, the system now enables real-time performance monitoring, metric visualization, and trace inspection for each prediction request.

The upgraded FastAPI server records:
- Prediction metrics for Prometheus scraping
- Traces with custom attributes (e.g., prediction values, model version, timestamp)
- End-to-end visibility from incoming request to model inference


## What This Project Includes

Prometheus integration

- `/metrics` endpoint automatically instrumented
- `model_prediction_value` metric for monitoring prediction outputs
- Exposed on `localhost:8000/metrics`

Grafana dashboard

- Visualizes prediction metrics from Prometheus
- Uses PromQL query: `model_prediction_value`
- Real-time chart created under `localhost:3000`

OpenTelemetry + Jaeger tracing

- Each `/predict` request generates a trace viewable in Jaeger UI (`localhost:16686`)
- Includes `POST /predict` operation and custom `span model_prediction`
- Recorded attributes:
  - `prediction.value`
  - `model.version`
  - `timestamp.utc`

FastAPI Instrumentation

- Automatic request/response tracing via `FastAPIInstrumentor`
- Manual span tracking for inference logic

**Example FastAPI URL:**  
`http://127.0.0.1:8000/docs`

**Example Request**
`
curl -X 'POST' 'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "crim": 0.03,
  "zn": 25.0,
  "indus": 5.1,
  "chas": 0,
  "nox": 0.45,
  "rm": 6.5,
  "age": 65.2,
  "dis": 4.8,
  "rad": 5.0,
  "tax": 290.0,
  "ptratio": 17.8,
  "b": 390.5,
  "lstat": 9.3
}'
`

**Example Response**

`
{
  "prediction": 24.38,
  "metadata": {
    "app_version": "0.2.0",
    "model_version": "models:/a2-demo-model/latest",
    "timestamp_utc": "2025-11-12T21:58:14Z"
  }
}
`

### Observability Tools
| Tool |	Purpose	| Local URL |
|-----|-----------|-----------|
| Prometheus	| Collects metrics from FastAPI |	http://localhost:9090 |
| Grafana	| Visualizes metrics (PromQL: model_prediction_value)	| http://localhost:3000 |
| Jaeger	| Displays distributed traces |	http://localhost:16686 |

## Reflections
### What Was Easy
- Setting up Prometheus scraping and exposing /metrics
- Using Grafana to visualize prediction results dynamically
- Adding Jaeger exporter through OpenTelemetry SDK

### What Was Hard
- Fixing middleware order (instrumentation before app startup)
- Configuring Jaeger agent and Docker network connections
- Troubleshooting firewall blocking the UDP port 6831
- Ensuring traces correctly display under the service name fastapi-mlops-a3


## Resources Used
- OpenTelemetry FastAPI Instrumentation Docs
- Prometheus FastAPI Instrumentator
- Jaeger All-in-One Docker Image
- Assignment guide
- ChatGPT for debugging observability stack integration and trace validation