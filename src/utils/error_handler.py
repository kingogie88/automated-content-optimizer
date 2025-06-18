import logging
import sys
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import traceback
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class GEOError(Exception):
    """Base exception for GEO AI Optimizer"""
    def __init__(self, message: str, code: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class EntityExtractionError(GEOError):
    """Error during entity extraction"""
    pass

class SchemaGenerationError(GEOError):
    """Error during schema generation"""
    pass

class DistributionError(GEOError):
    """Error during content distribution"""
    pass

class APIError(GEOError):
    """Error during API operations"""
    pass

ERROR_CODES = {
    'ENTITY_EXTRACTION_FAILED': 'Failed to extract entities from content',
    'WIKIDATA_LINKING_FAILED': 'Failed to link entities to Wikidata',
    'SCHEMA_GENERATION_FAILED': 'Failed to generate schema',
    'SCHEMA_VALIDATION_FAILED': 'Failed to validate schema',
    'DISTRIBUTION_FAILED': 'Failed to distribute content',
    'API_ERROR': 'API operation failed',
    'INVALID_INPUT': 'Invalid input provided',
    'RATE_LIMIT_EXCEEDED': 'Rate limit exceeded',
    'AUTHENTICATION_FAILED': 'Authentication failed',
    'PERMISSION_DENIED': 'Permission denied'
}

def log_error(error: Exception, request: Optional[Request] = None) -> None:
    """Log error with context"""
    error_context = {
        'timestamp': datetime.utcnow().isoformat(),
        'error_type': error.__class__.__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc()
    }
    
    if request:
        error_context.update({
            'method': request.method,
            'url': str(request.url),
            'client_host': request.client.host if request.client else None,
            'headers': dict(request.headers)
        })
    
    logger.error(json.dumps(error_context))

async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler for FastAPI"""
    if isinstance(exc, GEOError):
        log_error(exc, request)
        return JSONResponse(
            status_code=400,
            content={
                'error': {
                    'code': exc.code,
                    'message': exc.message,
                    'details': exc.details
                }
            }
        )
    elif isinstance(exc, HTTPException):
        log_error(exc, request)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': {
                    'code': 'HTTP_ERROR',
                    'message': exc.detail
                }
            }
        )
    else:
        log_error(exc, request)
        return JSONResponse(
            status_code=500,
            content={
                'error': {
                    'code': 'INTERNAL_SERVER_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }
        )

def handle_entity_extraction_error(func):
    """Decorator for handling entity extraction errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise EntityExtractionError(
                message=ERROR_CODES['ENTITY_EXTRACTION_FAILED'],
                code='ENTITY_EXTRACTION_FAILED',
                details={'original_error': str(e)}
            )
    return wrapper

def handle_schema_generation_error(func):
    """Decorator for handling schema generation errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise SchemaGenerationError(
                message=ERROR_CODES['SCHEMA_GENERATION_FAILED'],
                code='SCHEMA_GENERATION_FAILED',
                details={'original_error': str(e)}
            )
    return wrapper

def handle_distribution_error(func):
    """Decorator for handling distribution errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise DistributionError(
                message=ERROR_CODES['DISTRIBUTION_FAILED'],
                code='DISTRIBUTION_FAILED',
                details={'original_error': str(e)}
            )
    return wrapper 