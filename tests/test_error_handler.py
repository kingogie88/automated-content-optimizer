import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.testclient import TestClient
from src.utils.error_handler import (
    GEOError,
    EntityExtractionError,
    SchemaGenerationError,
    DistributionError,
    APIError,
    error_handler,
    handle_entity_extraction_error,
    handle_schema_generation_error,
    handle_distribution_error,
    log_error
)
import logging
import json
from unittest.mock import patch, MagicMock

# Test data
SAMPLE_ERROR_MESSAGE = "Test error message"
SAMPLE_ERROR_CODE = "TEST_ERROR"
SAMPLE_ERROR_DETAILS = {"test": "details"}

# Create test app
app = FastAPI()
app.add_exception_handler(Exception, error_handler)

@app.get("/test-geo-error")
async def test_geo_error():
    raise GEOError(SAMPLE_ERROR_MESSAGE, SAMPLE_ERROR_CODE, SAMPLE_ERROR_DETAILS)

@app.get("/test-http-error")
async def test_http_error():
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/test-unexpected-error")
async def test_unexpected_error():
    raise ValueError("Unexpected error")

# Test client
client = TestClient(app)

def test_geo_error_handler():
    """Test handling of GEOError"""
    response = client.get("/test-geo-error")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == SAMPLE_ERROR_CODE
    assert data["error"]["message"] == SAMPLE_ERROR_MESSAGE
    assert data["error"]["details"] == SAMPLE_ERROR_DETAILS

def test_http_error_handler():
    """Test handling of HTTPException"""
    response = client.get("/test-http-error")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"
    assert data["error"]["message"] == "Not found"

def test_unexpected_error_handler():
    """Test handling of unexpected errors"""
    response = client.get("/test-unexpected-error")
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "An unexpected error occurred" in data["error"]["message"]

def test_entity_extraction_error():
    """Test EntityExtractionError"""
    error = EntityExtractionError(
        message="Entity extraction failed",
        code="ENTITY_EXTRACTION_FAILED",
        details={"text": "sample text"}
    )
    assert isinstance(error, GEOError)
    assert error.message == "Entity extraction failed"
    assert error.code == "ENTITY_EXTRACTION_FAILED"
    assert error.details == {"text": "sample text"}

def test_schema_generation_error():
    """Test SchemaGenerationError"""
    error = SchemaGenerationError(
        message="Schema generation failed",
        code="SCHEMA_GENERATION_FAILED",
        details={"schema": "sample schema"}
    )
    assert isinstance(error, GEOError)
    assert error.message == "Schema generation failed"
    assert error.code == "SCHEMA_GENERATION_FAILED"
    assert error.details == {"schema": "sample schema"}

def test_distribution_error():
    """Test DistributionError"""
    error = DistributionError(
        message="Distribution failed",
        code="DISTRIBUTION_FAILED",
        details={"platform": "test platform"}
    )
    assert isinstance(error, GEOError)
    assert error.message == "Distribution failed"
    assert error.code == "DISTRIBUTION_FAILED"
    assert error.details == {"platform": "test platform"}

@patch('src.utils.error_handler.logger')
def test_log_error(mock_logger):
    """Test error logging"""
    error = GEOError(SAMPLE_ERROR_MESSAGE, SAMPLE_ERROR_CODE, SAMPLE_ERROR_DETAILS)
    request = MagicMock(spec=Request)
    request.method = "GET"
    request.url = "http://test.com"
    request.client.host = "127.0.0.1"
    request.headers = {"test": "header"}
    
    log_error(error, request)
    
    mock_logger.error.assert_called_once()
    log_data = json.loads(mock_logger.error.call_args[0][0])
    assert "timestamp" in log_data
    assert log_data["error_type"] == "GEOError"
    assert log_data["error_message"] == SAMPLE_ERROR_MESSAGE
    assert "traceback" in log_data
    assert log_data["method"] == "GET"
    assert log_data["url"] == "http://test.com"
    assert log_data["client_host"] == "127.0.0.1"
    assert log_data["headers"] == {"test": "header"}

def test_entity_extraction_error_decorator():
    """Test entity extraction error decorator"""
    @handle_entity_extraction_error
    def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(EntityExtractionError) as exc_info:
        test_func()
    
    assert exc_info.value.code == "ENTITY_EXTRACTION_FAILED"
    assert "Failed to extract entities from content" in exc_info.value.message
    assert "Test error" in exc_info.value.details["original_error"]

def test_schema_generation_error_decorator():
    """Test schema generation error decorator"""
    @handle_schema_generation_error
    def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(SchemaGenerationError) as exc_info:
        test_func()
    
    assert exc_info.value.code == "SCHEMA_GENERATION_FAILED"
    assert "Failed to generate schema" in exc_info.value.message
    assert "Test error" in exc_info.value.details["original_error"]

def test_distribution_error_decorator():
    """Test distribution error decorator"""
    @handle_distribution_error
    def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(DistributionError) as exc_info:
        test_func()
    
    assert exc_info.value.code == "DISTRIBUTION_FAILED"
    assert "Failed to distribute content" in exc_info.value.message
    assert "Test error" in exc_info.value.details["original_error"] 