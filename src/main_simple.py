"""
Simplified FastAPI application for CI testing.
This version avoids heavy dependencies and focuses on core functionality.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uvicorn

# Use simplified processors
from src.core.content_processor_simple import SimpleContentProcessor
from src.core.seo_optimizer import SEOOptimizer

app = FastAPI(
    title="Content Optimization API (Simplified)",
    description="Simplified content processing and optimization API for CI testing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize processors
content_processor = SimpleContentProcessor()
seo_optimizer = SEOOptimizer()

@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"message": "Content Optimizer API (Simplified)"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/optimize")
async def optimize_content(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    target_platforms: Optional[List[str]] = Form(None),
    target_keywords: Optional[List[str]] = Form(None)
):
    """
    Optimize content for SEO and AI platforms.
    
    Args:
        text: Text content to optimize
        file: File to upload and optimize
        target_platforms: List of target platforms
        target_keywords: List of target keywords
        
    Returns:
        Optimization results
    """
    try:
        # Get content from text or file
        content = ""
        if text:
            content = text
        elif file:
            # Save uploaded file
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process the file
            result = content_processor.process_content(file_path)
            content = result.get("content", "")
            
            # Clean up
            os.unlink(file_path)
        else:
            raise HTTPException(status_code=400, detail="No content provided")
        
        if not content:
            raise HTTPException(status_code=400, detail="Empty content")
        
        # Process content
        content_analysis = content_processor.process_content(content)
        
        # SEO optimization
        seo_result = seo_optimizer.optimize_content(
            content=content,
            target_keywords=target_keywords or []
        )
        
        # Simplified GEO optimization (mock)
        geo_optimization = {
            "score": 85.0,
            "suggestions": ["Content is well-structured for AI platforms"],
            "metrics": {
                "context_clarity": 80.0,
                "factual_consistency": 90.0
            }
        }
        
        return {
            "content_analysis": content_analysis,
            "seo_optimization": seo_result,
            "geo_optimization": geo_optimization
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("src.main_simple:app", host="0.0.0.0", port=8000, reload=True) 