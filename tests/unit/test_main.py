import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "config" in data
    assert "metrics" in data

def test_supported_formats():
    response = client.get("/supported-formats")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert "video" in data
    assert "audio" in data
    assert "documents" in data

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict) 