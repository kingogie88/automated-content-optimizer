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
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

def test_optimize_text_content():
    """Test optimizing text content."""
    response = client.post(
        "/api/optimize",
        data={
            "text": "This is a test article for optimization.",
            "target_keywords": ["test", "article"],
            "target_platforms": ["chatgpt"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "content_analysis" in data
    assert "seo_optimization" in data
    assert "geo_optimization" in data

def test_optimize_file_content():
    """Test optimizing file content."""
    test_content = "This is test content from a file."
    
    response = client.post(
        "/api/optimize",
        files={"file": ("test.txt", test_content, "text/plain")},
        data={
            "target_keywords": ["test"],
            "target_platforms": ["claude"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "content_analysis" in data
    assert "seo_optimization" in data
    assert "geo_optimization" in data

def test_optimize_with_image(sample_image):
    """Test optimizing content with image file."""
    response = client.post(
        "/api/optimize",
        files={"file": ("test.png", sample_image, "image/png")},
        data={
            "target_keywords": ["image", "test"],
            "target_platforms": ["chatgpt"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "content_analysis" in data
    assert "seo_optimization" in data
    assert "geo_optimization" in data

def test_error_handling_empty_content():
    """Test error handling for empty content."""
    response = client.post(
        "/api/optimize",
        data={
            "text": "",
            "target_platforms": ["chatgpt"]
        }
    )
    # Should handle empty content gracefully
    assert response.status_code in [200, 400, 422]

def test_error_handling_no_content():
    """Test error handling when no content is provided."""
    response = client.post(
        "/api/optimize",
        data={
            "target_platforms": ["chatgpt"]
        }
    )
    # Should handle missing content gracefully
    assert response.status_code in [200, 400, 422] 