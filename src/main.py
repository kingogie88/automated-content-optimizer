from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
from pathlib import Path
import shutil
import asyncio
from datetime import datetime

from core.content_processor import MultiModalProcessor
from config.multimodal_config import ProcessingConfig
from middleware.security import security_middleware, SecurityValidator
from utils.logging_config import setup_logger
from utils.monitoring import PerformanceMonitor

# Initialize components
logger = setup_logger("content_optimizer")
monitor = PerformanceMonitor()
security_validator = SecurityValidator()

app = FastAPI(
    title="Content Optimization API",
    description="Multi-modal content processing and optimization API",
    version="1.0.0"
)

# Add middleware
app.middleware("http")(security_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processor and config
config = ProcessingConfig()
config.optimize_for_hardware()
processor = MultiModalProcessor()

# Create required directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/process")
async def process_content(
    request: Request,
    text: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    audio_files: Optional[List[UploadFile]] = File(None),
    video_files: Optional[List[UploadFile]] = File(None),
    structured_data: Optional[str] = Form(None)
):
    """
    Process multiple types of content simultaneously.
    """
    # Start monitoring request
    start_time = monitor.start_request()
    
    try:
        # Create session directory
        session_dir = UPLOAD_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir.mkdir(exist_ok=True)
        
        # Process files
        saved_files = {
            "images": [],
            "audio": [],
            "video": []
        }
        
        try:
            # Save and validate files
            if images:
                for img in images:
                    file_path = session_dir / f"image_{img.filename}"
                    with file_path.open("wb") as f:
                        shutil.copyfileobj(img.file, f)
                    await security_validator.validate_file(str(file_path))
                    saved_files["images"].append(str(file_path))
            
            if audio_files:
                for audio in audio_files:
                    file_path = session_dir / f"audio_{audio.filename}"
                    with file_path.open("wb") as f:
                        shutil.copyfileobj(audio.file, f)
                    await security_validator.validate_file(str(file_path))
                    saved_files["audio"].append(str(file_path))
            
            if video_files:
                for video in video_files:
                    file_path = session_dir / f"video_{video.filename}"
                    with file_path.open("wb") as f:
                        shutil.copyfileobj(video.file, f)
                    await security_validator.validate_file(str(file_path))
                    saved_files["video"].append(str(file_path))
            
            # Parse structured data
            parsed_data = json.loads(structured_data) if structured_data else None
            
            # Process content
            result = await processor.process_content(
                text=text,
                images=saved_files["images"] if saved_files["images"] else None,
                audio_files=saved_files["audio"] if saved_files["audio"] else None,
                video_files=saved_files["video"] if saved_files["video"] else None,
                structured_data=parsed_data
            )
            
            logger.info(f"Successfully processed content for session {session_dir.name}")
            
            return {
                "status": "success",
                "data": {
                    "text": result.text,
                    "images": result.images,
                    "audio_transcripts": result.audio_transcripts,
                    "video_metadata": result.video_metadata,
                    "structured_data": result.structured_data
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
            
        finally:
            # Clean up uploaded files
            if session_dir.exists():
                shutil.rmtree(session_dir)
            
    finally:
        # End monitoring
        monitor.end_request(start_time)

@app.get("/health")
async def health_check():
    """Check API health and configuration status."""
    metrics = monitor.get_current_metrics()
    return {
        "status": "healthy",
        "config": config.to_dict(),
        "gpu_available": config.use_gpu,
        "workers": config.num_workers,
        "metrics": metrics
    }

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics summary."""
    return monitor.get_metrics_summary()

@app.get("/supported-formats")
async def get_supported_formats():
    """Get information about supported file formats."""
    return {
        "images": config.supported_image_formats,
        "video": config.supported_video_formats,
        "audio": config.supported_audio_formats,
        "documents": config.supported_document_formats
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    monitor.stop()
    logger.info("Application shutting down") 