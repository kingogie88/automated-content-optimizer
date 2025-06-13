import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
import io
from PIL import Image
import numpy as np

from src.main import app

client = TestClient(app)

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img_data = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_data)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

@pytest.fixture
def sample_text():
    return "This is a sample article for testing content optimization."

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "config" in data
    assert "metrics" in data

def test_supported_formats():
    """Test the supported formats endpoint."""
    response = client.get("/supported-formats")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert "video" in data
    assert "audio" in data
    assert "documents" in data

def test_metrics():
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "avg_response_time_ms" in data

def test_process_text():
    """Test processing text content."""
    response = client.post(
        "/process",
        data={
            "text": "This is a test article."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["text"]

def test_process_image(sample_image):
    """Test processing image content."""
    response = client.post(
        "/process",
        files={
            "images": ("test.png", sample_image, "image/png")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["images"]

def test_process_multiple_content_types(sample_image, sample_text):
    """Test processing multiple content types together."""
    response = client.post(
        "/process",
        data={
            "text": sample_text,
            "structured_data": json.dumps({"key": "value"})
        },
        files={
            "images": ("test.png", sample_image, "image/png")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["text"]
    assert data["data"]["images"]
    assert data["data"]["structured_data"]

def test_rate_limiting():
    """Test rate limiting middleware."""
    # Make multiple requests quickly
    responses = []
    for _ in range(70):  # More than the default 60 requests per minute
        response = client.get("/health")
        responses.append(response.status_code)
    
    # Should see some 429 responses
    assert 429 in responses

def test_file_size_limit(sample_image):
    """Test file size limit validation."""
    # Create a large file
    large_img_data = np.random.randint(0, 255, (5000, 5000, 3), dtype=np.uint8)
    large_img = Image.fromarray(large_img_data)
    img_byte_arr = io.BytesIO()
    large_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    response = client.post(
        "/process",
        files={
            "images": ("large.png", img_byte_arr, "image/png")
        }
    )
    assert response.status_code == 400
    assert "file size" in response.json()["detail"].lower()

def test_invalid_file_type():
    """Test invalid file type validation."""
    # Create an invalid file
    invalid_file = io.BytesIO(b"invalid file content")
    
    response = client.post(
        "/process",
        files={
            "images": ("test.txt", invalid_file, "text/plain")
        }
    )
    assert response.status_code == 400
    assert "file type" in response.json()["detail"].lower()

def test_error_handling():
    """Test error handling for invalid input."""
    response = client.post(
        "/process",
        data={
            "structured_data": "invalid json"
        }
    )
    assert response.status_code == 200  # API returns 200 with error status
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data 