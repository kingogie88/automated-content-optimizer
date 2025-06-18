from fastapi import APIRouter, HTTPException
from src.core.analytics_manager import AnalyticsManager
from src.utils.error_handler import handle_entity_extraction_error, EntityExtractionError

router = APIRouter()
analytics_manager = AnalyticsManager()

@router.get("/summary")
async def get_analytics_summary():
    """Get analytics summary"""
    try:
        summary = analytics_manager.get_summary()
        return summary
    except Exception as e:
        raise EntityExtractionError(
            message="Failed to get analytics summary",
            code="ANALYTICS_FAILED",
            details={"error": str(e)}
        )

@router.get("/status")
async def get_status():
    """Get analytics status"""
    return {"status": "operational"} 