import pytest
from fastapi.testclient import TestClient
from src.main import app
import json
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to GEO AI Optimizer"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

@patch('src.main.logger')
def test_request_logging(mock_logger):
    """Test request logging middleware"""
    response = client.get("/")
    assert response.status_code == 200
    
    # Check if request was logged
    mock_logger.info.assert_any_call("Request: GET http://testserver/")
    # Check if response was logged
    mock_logger.info.assert_any_call("Response: 200")

def test_error_handling():
    """Test error handling middleware"""
    # Test with a non-existent endpoint
    response = client.get("/non-existent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"

def test_cors_headers():
    """Test CORS headers"""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_content_router():
    """Test content router endpoints"""
    # Test content optimization endpoint
    test_content = {
        "text": "Sample content for testing",
        "type": "article"
    }
    response = client.post("/api/content/optimize", json=test_content)
    assert response.status_code in [200, 400]  # Either success or validation error

def test_distribution_router():
    """Test distribution router endpoints"""
    # Test distribution status endpoint
    response = client.get("/api/distribution/status")
    assert response.status_code in [200, 400]  # Either success or validation error

def test_analytics_router():
    """Test analytics router endpoints"""
    # Test analytics summary endpoint
    response = client.get("/api/analytics/summary")
    assert response.status_code in [200, 400]  # Either success or validation error

@patch('src.main.logger')
def test_error_logging(mock_logger):
    """Test error logging"""
    # Make a request that will cause an error
    response = client.get("/non-existent")
    assert response.status_code == 404
    
    # Check if error was logged
    mock_logger.error.assert_called()
    error_log = mock_logger.error.call_args[0][0]
    assert "Error processing request" in error_log 