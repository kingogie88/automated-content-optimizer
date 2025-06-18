import pytest
from fastapi.testclient import TestClient

from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_optimize_content_text(client):
    """Test content optimization endpoint with text"""
    content = "Test content for optimization"
    response = client.post(
        "/api/optimize",
        data={
            "text": content,
            "target_platforms": ["chatgpt", "claude"],
            "target_keywords": ["test", "optimization"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "content_analysis" in data
    assert "seo_optimization" in data
    assert "geo_optimization" in data

def test_optimize_content_file(client):
    """Test content optimization endpoint with file upload"""
    # Create a simple text file for testing
    test_content = "Test content for file optimization"
    
    response = client.post(
        "/api/optimize",
        files={"file": ("test.txt", test_content, "text/plain")},
        data={
            "target_platforms": ["chatgpt"],
            "target_keywords": ["test"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "content_analysis" in data
    assert "seo_optimization" in data
    assert "geo_optimization" in data

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200

def test_error_handling_invalid_content(client):
    """Test error handling for invalid content"""
    response = client.post(
        "/api/optimize",
        data={
            "text": "",  # Empty content
            "target_platforms": ["chatgpt"]
        }
    )
    
    # Should handle empty content gracefully
    assert response.status_code in [200, 400, 422] 