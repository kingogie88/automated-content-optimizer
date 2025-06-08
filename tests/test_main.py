import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_docs():
    """Test the OpenAPI docs endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_optimization_endpoint_unauthorized():
    """Test that optimization endpoint requires authentication"""
    response = client.post("/api/v1/optimize", json={
        "content": "Test content",
        "optimization_type": "seo"
    })
    assert response.status_code == 401  # Unauthorized without token

def test_optimization_endpoint_authorized():
    """Test optimization endpoint with mock token"""
    response = client.post(
        "/api/v1/optimize",
        headers={"Authorization": "Bearer test_token"},
        json={
            "content": "Test content",
            "optimization_type": "seo"
        }
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "success" 