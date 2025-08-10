# MLOps Iris Pipeline

A comprehensive MLOps pipeline for the Iris dataset classification problem, featuring automated training, model versioning, API deployment, and monitoring with Prometheus and Grafana.

## Overview

This project demonstrates a complete MLOps workflow including:
- Automated model training and evaluation
- Model versioning with MLflow
- REST API deployment with FastAPI
- Containerization with Docker
- Monitoring and observability with Prometheus and Grafana
- CI/CD pipeline integration

## Prerequisites

- Python 3.12.0
- Docker Desktop
- WSL2 (for Windows users)
- PowerShell (Admin mode for Windows setup)

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install setuptools
```

### 2. MLflow Server Setup

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root file:/mlruns \
  --host 0.0.0.0 --port 5000
```

### 3. Docker Setup (Windows)

If you're on Windows, install WSL2 and Docker Desktop:

```powershell
# Install WSL2 (run in PowerShell as Administrator)
wsl --install
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/

## Usage

### Model Training

```bash
# Train models
python src/train.py
```

### API Deployment

#### Option 1: Docker Container

```bash
# Build Docker image
docker build -t iris-api:latest -f Dockerfile .

# Run container
docker run -d --name iris-api-demo -p 8000:8000 iris-api:latest

# Check container status
docker ps -a --filter name=iris-api-demo

# View logs
docker logs -f iris-api-demo
```

#### Option 2: Docker Compose (Full Stack)

```bash
# Deploy API + Prometheus + Grafana
docker compose up -d
```

### API Testing

#### PowerShell Example
```powershell
$body = @{
    sepal_length=5.1
    sepal_width=3.5
    petal_length=1.4
    petal_width=0.2
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -ContentType application/json -Body $body
```

#### cURL Example
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## Monitoring

### Prometheus
- Metrics endpoint: http://localhost:9090
- Collects API performance metrics and model predictions

### Grafana
- Dashboard: http://localhost:3000
- Access Credentials:  admin/admin@123
- Default credentials: admin/admin
- Pre-configured dashboard for Iris model monitoring

### MLflow
- Tracking server: http://localhost:5000
- Model registry and experiment tracking

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Make predictions
- `GET /metrics` - Prometheus metrics

## Model Information

The pipeline trains multiple models:
- Decision Tree (baseline and feature-engineered)
- LightGBM (baseline and feature-engineered)
- Random Forest
- Support Vector Machine
- Logistic Regression

Models are automatically evaluated and the best performing model is selected for deployment.

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Troubleshooting

### Common Issues

1. **Docker build fails**: Ensure Docker Desktop is running and WSL2 is properly configured
2. **Port conflicts**: Check if ports 8000, 5000, 9090, or 3000 are already in use
3. **MLflow connection issues**: Verify the MLflow server is running on port 5000

### Cleanup Commands

Docker link - https://hub.docker.com/layers/saikrithik/iris-api/latest/images/sha256-2bfc85b4a7d41d2091f184b6de25a975f238290db93091638d582c32f7685b52

```bash
# Remove Docker container
docker rm -f iris-api-demo

# Stop all services
docker compose down

# Clean up Docker images
docker rmi iris-api:latest
```
