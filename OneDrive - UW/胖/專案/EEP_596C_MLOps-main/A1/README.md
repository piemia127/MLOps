# A1: Deploy LASSO Regression Model with FastAPI on AWS

## Summary
This project extends **A0’s LASSO Regression model** and deploys it into production using **FastAPI**, **Docker**, and **AWS ECS (Fargate)**.  
The goal is to expose the trained model through a public REST API so that anyone can send requests to `/predict` and receive real-time predictions from the internet.

This deployment demonstrates the full MLOps workflow — containerizing a model, hosting it on the cloud, and enable CI/CD via GitHub Actions.

---

## What This Project Includes

- FastAPI Application serving the /predict endpoint
- Docker Container that runs uvicorn inside a lightweight Python image
- Trained LASSO Regression Model (model.pkl) exported from A0 with normalization parameters (mu, sigma, w, b)
- AWS ECR Repository hosting the image
- AWS ECS Fargate Service providing a publicly accessible endpoint
- GitHub Actions Pipeline for automated build, push, and deploy upon each code update


**Base URL:**  
`http://54.244.60.194:8000/docs`

**Example Request (via cURL)**

`
curl -X 'POST' \
  'http://54.244.60.194:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "crim": 0.00632,
  "zn": 18.0,
  "indus": 2.31,
  "chas": 0.0,
  "nox": 0.538,
  "rm": 6.575,
  "age": 65.2,
  "dis": 4.09,
  "rad": 1.0,
  "tax": 296.0,
  "ptratio": 15.3,
  "b": 396.9,
  "lstat": 4.98
}'
`

**Expected Response:**

`
{"prediction": xx.xx}
`

## Reflections
### What Was Easy
- Running the FastAPI app locally with uvicorn
- Using Docker to containerize the model and test it on my machine

### What Was Hard
- Configuring AWS permissions and understanding security groups(this got me crazy)

- I spent a long time debugging why the predictions were extremely off, and eventually realized it was because I hadn’t applied the same normalization during inference as I did during training.

### Collaboration
- Daniel Tseng
- Chia-En Wu

Earlier discussions from A0 carried over, especially about feature normalization and LASSO behavior.

## Resources Used
- AWS Documentation (ECR & ECS Fargate setup)
- FastAPI official docs
- GitHub Actions guide: Build & Push Docker Image to AWS ECR
- ChatGPT (for deployment debugging and explanation of AWS configurations)