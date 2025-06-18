from fastapi import APIRouter, HTTPException
from src.core.distribution_manager import DistributionManager
from src.utils.error_handler import handle_distribution_error, DistributionError

router = APIRouter()
distribution_manager = DistributionManager()

@router.post("/publish")
@handle_distribution_error
async def publish_content(content: str, platform: str):
    """Publish content to specified platform"""
    try:
        result = distribution_manager.publish_content(content, platform)
        return result
    except Exception as e:
        raise DistributionError(
            message="Failed to publish content",
            code="PUBLISH_FAILED",
            details={"error": str(e), "platform": platform}
        )

@router.get("/status")
async def get_status():
    """Get distribution status"""
    return {"status": "operational"} 