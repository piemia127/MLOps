# HW2 Deployment Notes

This document records how I built, containerized, and deployed my FastAPI model application using Docker, AWS ECS, and GitHub Actions.

## 1. Local Build and Test

Before deployment, the FastAPI app was tested locally.

### Steps
```
docker build -t a1-fastapi .
docker run -d -p 8000:8000 a1-fastapi
```
Visit
http://127.0.0.1:8000/docs
to confirm that the /predict endpoint works.

## 2. AWS ECR Setup
Commands

```
aws ecr create-repository --repository-name a1-fastapi --region us-west-2
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 033877255068.dkr.ecr.us-west-2.amazonaws.com
docker tag a1-fastapi:latest 033877255068.dkr.ecr.us-west-2.amazonaws.com/a1-fastapi:latest
docker push 033877255068.dkr.ecr.us-west-2.amazonaws.com/a1-fastapi:latest
```
Confirmed that the image appears in the ECR console.

## 3. AWS ECS Setup
Configuration:

- Cluster: mlops-A1-cluster
- Service: fastapi-service
- Launch type: Fargate
- Container port: 8000
- Security group:
  - Inbound: TCP 8000 from 0.0.0.0/0
  - Outbound: All traffic (0.0.0.0/0)

Fixed error uvicorn not found by adding dependencies to requirements.txt.

## 4. GitHub Actions Automation
Workflow file location: .github/workflows/deploy.yml

Pipeline Steps:

- Checkout repository
- Configure AWS credentials
- Login to ECR
- Build and push Docker image
- Deploy new image to ECS

GitHub Secrets:
| Key	| Description |
|-----|-------------|
| AWS_ACCESS_KEY_ID |	IAM user access key|
| AWS_SECRET_ACCESS_KEY	| IAM secret key|
| AWS_REGION |	us-west-2|
| ECR_REPOSITORY	| 033877255068.dkr.ecr.us-west-2.amazonaws.com/a1-fastapi|
| ECS_CLUSTER	| mlops-A1-cluster|
| ECS_SERVICE |	fastapi-service|

## 5. Deployment Verification
URL:
http://54.244.60.194:8000/docs

Confirmed that the FastAPI Swagger UI loads and returns a valid prediction.

## 6. Troubleshooting Notes
| Issue	| Cause	| Solution |
|-------|-------|----------|
| uvicorn not found | Empty requirements.txt	| Added FastAPI and Uvicorn |
| ECS cannot pull image |	Missing outbound rule |	Allowed 0.0.0.0/0 outbound
| Dockerfile path error	| File not in repo root	| Moved Dockerfile to root
| Weird prediction result | Normalization missing | Includes normalization parameters (mu and sigma).


## 7. Final Status
| Component	| Status |
|-----------|--------|
|FastAPI App |	Running
|Docker Image	| Uploaded
|ECS Service | Active
|GitHub Actions |	Automated
