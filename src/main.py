from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uvicorn
from src.utils.error_handler import error_handler, GEOError
from src.routers import content, distribution, analytics
import logging

from src.core.content_processor import ContentProcessor
from src.core.seo_optimizer import SEOOptimizer
from src.core.geo_optimizer import GEOOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="GEO AI Optimizer",
    description="AI-powered content optimization and distribution platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

content_processor = ContentProcessor()
seo_optimizer = SEOOptimizer()
geo_optimizer = GEOOptimizer()

# Add error handler
app.add_exception_handler(Exception, error_handler)

# Include routers
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(distribution.router, prefix="/api/distribution", tags=["distribution"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to GEO AI Optimizer",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "config": {
            "environment": "development",
            "debug": True
        }
    }

@app.get("/api/metrics")
async def get_metrics():
    """Get application metrics"""
    return {
        "requests_processed": 0,
        "errors_count": 0,
        "uptime": "0:00:00",
        "memory_usage": "0 MB"
    }

@app.get("/supported-formats")
async def get_supported_formats():
    """Get supported file formats"""
    return {
        "text": [".txt", ".md", ".html"],
        "documents": [".pdf", ".doc", ".docx"],
        "images": [".jpg", ".jpeg", ".png", ".gif"],
        "audio": [".mp3", ".wav", ".m4a"],
        "video": [".mp4", ".avi", ".mov"]
    }

@app.post("/api/optimize")
async def optimize_content(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    target_platforms: Optional[List[str]] = Form(None),
    target_keywords: Optional[List[str]] = Form(None)
):
    try:
        if file:
            file_path = UPLOAD_DIR / file.filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            content_result = content_processor.process_content(str(file_path))
            content = content_result["content"]
            os.remove(file_path)
        else:
            content = text
            content_result = content_processor.process_content(content)
        seo_result = seo_optimizer.optimize_content(
            content=content,
            target_keywords=target_keywords or []
        )
        geo_result = geo_optimizer.optimize_content(
            content=content,
            target_platforms=target_platforms or []
        )
        return {
            "content_analysis": content_result,
            "seo_optimization": seo_result,
            "geo_optimization": geo_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True) 