import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    """Test the prediction endpoint with valid data."""
    test_data = {
        "features": {
            "feature1": 1.0,
            "feature2": 2.0,
            "feature3": 3.0,
            "feature4": 4.0
        }
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probability" in response.json()
    assert "confidence" in response.json()

def test_predict_invalid_data():
    """Test the prediction endpoint with invalid data."""
    test_data = {
        "features": {}
    }
    response = client.post("/predict", json=test_data)
    assert response.status_code in [400, 422]

def test_model_info():
    """Test the model info endpoint."""
    response = client.get("/model/info")
    assert response.status_code == 200
    assert "model_type" in response.json()
    assert "model_path" in response.json()

def test_metrics_endpoint():
    """Test that metrics endpoint is available."""
    response = client.get("/metrics")
    assert response.status_code == 200

def test_predict_batch():
    """Test batch prediction if endpoint exists."""
    test_data = {
        "instances": [
            {
                "feature1": 1.0,
                "feature2": 2.0,
                "feature3": 3.0,
                "feature4": 4.0
            },
            {
                "feature1": 2.0,
                "feature2": 3.0,
                "feature3": 4.0,
                "feature4": 5.0
            }
        ]
    }
    response = client.post("/predict/batch", json=test_data)
    # Accept both 200 (implemented) and 404 (not implemented yet)
    assert response.status_code in [200, 404]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
