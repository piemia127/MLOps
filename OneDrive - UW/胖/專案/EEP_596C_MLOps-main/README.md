# MLOps Coursework Repository

This repository contains a series of assignments (**A0–A2**, with **A3–A4** planned) that progressively build a complete **MLOps workflow** — from model development to deployment, versioning, and monitoring.

| Assignment | Core Topic | Description |
|-------------|-------------|-------------|
| **A0** | Linear, Ridge & LASSO Regression | Implemented from scratch using Python on the Boston Housing dataset. Covered gradient descent, cost function derivation, normalization, and regularization. |
| **A1** | Model Deployment with FastAPI & AWS | Containerized the trained LASSO model using Docker and deployed it to AWS ECS (Fargate) via GitHub Actions CI/CD pipeline, exposing a `/predict` REST API. |
| **A2** | Versioned Model Serving with MLflow | Integrated MLflow Model Registry into FastAPI to enable versioned model management and metadata-aware inference, supporting dynamic model selection. |
| **A3** | Observability | Instrumented the system with **OpenTelemetry** for distributed tracing in **Jaeger** (latency analysis) and configured **Prometheus** & **Grafana** for real-time metrics visualization (e.g., prediction values, throughput).|

---

### Repository Overview
This repo demonstrates the **end-to-end MLOps pipeline** — from data preprocessing and model training to automated deployment and versioned serving.

### Tech Stack
Python • FastAPI • Docker • AWS ECS/Fargate • GitHub Actions • MLflow • pytest

### Objective
> To build a reproducible, modular, and scalable MLOps workflow that bridges machine learning and production infrastructure.
