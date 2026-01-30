# 🚀 MLOps Production Pipeline

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Overview

A **production-grade MLOps pipeline** demonstrating industry best practices for deploying, monitoring, and maintaining machine learning models at scale. This project showcases the complete ML lifecycle with containerization, orchestration, CI/CD, and observability.

### 🌟 Key Highlights

- ✅ **FastAPI** REST API for model serving
- ✅ **Docker** multi-stage builds for optimized images
- ✅ **Kubernetes** deployment with auto-scaling
- ✅ **GitHub Actions** CI/CD pipeline
- ✅ **Prometheus & Grafana** for monitoring
- ✅ **Model versioning** and experiment tracking
- ✅ **Health checks** and graceful shutdowns
- ✅ **Security best practices** (non-root user, secrets management)

## 📦 Project Structure

```
MLOps-Production-Pipeline/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── ml_model.py          # ML model wrapper
│   └── config.py            # Configuration management
│
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Kubernetes service
│   ├── hpa.yaml             # Horizontal Pod Autoscaler
│   └── configmap.yaml       # ConfigMaps
│
├── .github/
│   └── workflows/
│       ├── ci-cd.yaml       # CI/CD pipeline
│       └── docker-publish.yaml
│
├── monitoring/
│   ├── prometheus.yaml      # Prometheus config
│   └── grafana-dashboard.json
│
├── tests/
│   ├── test_api.py          # API tests
│   └── test_model.py        # Model tests
│
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yaml      # Local development
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Kubernetes 1.24+ (or Minikube/Kind for local)
- Python 3.9+
- kubectl configured

### Local Development with Docker

```bash
# Clone the repository
git clone https://github.com/prakashkmr48/MLOps-Production-Pipeline.git
cd MLOps-Production-Pipeline

# Build and run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### Deploy to Kubernetes

```bash
# Build and push Docker image
docker build -t your-registry/mlops-api:v1.0 .
docker push your-registry/mlops-api:v1.0

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get svc mlops-api-service
```

## 💻 API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy", "model_loaded": true}
```

### Prediction
```bash
POST /predict
Body: {
  "features": [1.0, 2.0, 3.0, ...]
}
Response: {
  "prediction": 0.85,
  "model_version": "v1.2.0",
  "inference_time_ms": 12.5
}
```

### Model Info
```bash
GET /model/info
Response: {
  "name": "customer-churn-model",
  "version": "v1.2.0",
  "framework": "scikit-learn",
  "metrics": {...}
}
```

## 🐳 Docker Configuration

The Dockerfile uses **multi-stage builds** for optimization:

- **Stage 1 (Builder)**: Compiles dependencies
- **Stage 2 (Runtime)**: Minimal production image
- **Security**: Non-root user, minimal attack surface
- **Health checks**: Built-in container health monitoring

```bash
# Build optimized image
docker build -t mlops-api:latest .

# Run container
docker run -p 8000:8000 \n  -e MODEL_PATH=/app/models \n  mlops-api:latest
```

## ☘️ Kubernetes Deployment

### Features

- **Horizontal Pod Autoscaler (HPA)**: Auto-scaling based on CPU/memory
- **Resource limits**: CPU and memory constraints
- **Readiness/Liveness probes**: Health monitoring
- **ConfigMaps & Secrets**: Environment configuration
- **Rolling updates**: Zero-downtime deployments

```yaml
# Example scaling configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mlops-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mlops-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Automated pipeline with:

1. **Code Quality**: Linting and formatting checks
2. **Testing**: Unit and integration tests
3. **Security**: Vulnerability scanning
4. **Build**: Docker image creation
5. **Push**: Registry upload
6. **Deploy**: Kubernetes deployment

```yaml
# .github/workflows/ci-cd.yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/
      
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t mlops-api .
      - name: Deploy to Kubernetes
        run: kubectl apply -f k8s/
```

## 📊 Monitoring & Observability

### Prometheus Metrics

- Request latency (p50, p95, p99)
- Request count by endpoint
- Model inference time
- Error rates
- Resource utilization

### Grafana Dashboards

- API performance metrics
- Model performance tracking
- System health overview
- Alert configurations

```python
# Example: Custom metrics in FastAPI
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions')
latency_histogram = Histogram('prediction_latency_seconds', 'Prediction latency')

@app.post("/predict")
async def predict(request: PredictionRequest):
    with latency_histogram.time():
        result = model.predict(request.features)
    prediction_counter.inc()
    return result
```

## 🔒 Security Best Practices

- ✅ Non-root container user
- ✅ Secret management with Kubernetes Secrets
- ✅ Image vulnerability scanning
- ✅ Network policies
- ✅ RBAC for Kubernetes
- ✅ API authentication (JWT)
- ✅ Rate limiting

## 🧪 Testing

```bash
# Run unit tests
pytest tests/test_model.py -v

# Run integration tests
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=app tests/

# Load testing
locust -f tests/load_test.py --host=http://localhost:8000
```

## 📚 MLOps Best Practices Demonstrated

1. **Version Control**: Git for code, DVC for data/models
2. **Containerization**: Docker for reproducibility
3. **Orchestration**: Kubernetes for scalability
4. **CI/CD**: Automated testing and deployment
5. **Monitoring**: Prometheus + Grafana
6. **Model Versioning**: Semantic versioning
7. **Documentation**: Comprehensive README and API docs
8. **Testing**: Unit, integration, and load tests
9. **Security**: Industry-standard practices
10. **Observability**: Logging, metrics, tracing

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI |
| **Model Serving** | Python 3.9+ |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus + Grafana |
| **Testing** | Pytest, Locust |
| **Model Tracking** | MLflow |
| **Security** | Trivy, OWASP |

## 📝 Key Learnings

This project demonstrates:

- **Production-ready MLOps**: Complete pipeline from development to deployment
- **Scalability**: Kubernetes auto-scaling and load balancing
- **Reliability**: Health checks, graceful shutdowns, retry logic
- **Observability**: Comprehensive monitoring and logging
- **Security**: Multiple layers of security controls
- **DevOps Integration**: Seamless CI/CD workflow

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Prometheus Monitoring](https://prometheus.io/docs/)

## 💬 Contact

**Prakash Kumar**
- GitHub: [@prakashkmr48](https://github.com/prakashkmr48)
- Project: [MLOps-Production-Pipeline](https://github.com/prakashkmr48/MLOps-Production-Pipeline)

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## ⭐ Acknowledgments

- Built following industry MLOps best practices
- Designed for production scalability
- Optimized for interviewer demonstration

---

**👍 Ready for production deployment! Star this repo if you find it helpful!**
