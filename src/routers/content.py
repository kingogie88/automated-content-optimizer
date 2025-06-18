from fastapi import APIRouter, HTTPException
from src.core.content_processor import ContentProcessor
from src.utils.error_handler import handle_entity_extraction_error, EntityExtractionError

router = APIRouter()
content_processor = ContentProcessor()

@router.post("/optimize")
@handle_entity_extraction_error
async def optimize_content(text: str):
    """Optimize content for AI assistants"""
    try:
        result = content_processor.process_content(text)
        return result
    except Exception as e:
        raise EntityExtractionError(
            message="Failed to optimize content",
            code="CONTENT_OPTIMIZATION_FAILED",
            details={"error": str(e)}
        )

@router.get("/status")
async def get_status():
    """Get content processing status"""
    return {"status": "operational"} 