from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
import time

from database import get_db
from api.middleware.auth import get_current_user, requires_auth
from api.models.content import (
    SEOOptimizationRequest,
    GEOOptimizationRequest,
    CombinedOptimizationRequest,
    OptimizationResponse,
    OptimizationHistory,
    URLContent,
    FileContent
)
from core.seo.seo_optimizer import SEOOptimizer
from core.geo.geo_optimizer import GEOOptimizer
from database.models import Optimization, OptimizationSuggestion, User

router = APIRouter(
    prefix="/optimize",
    tags=["optimization"]
)

# Initialize optimizers
seo_optimizer = SEOOptimizer()
geo_optimizer = GEOOptimizer()

@router.post("/seo", response_model=OptimizationResponse)
async def optimize_seo(
    request: SEOOptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(requires_auth()),
    db: Session = Depends(get_db)
):
    """
    Optimize content for search engines
    """
    # Check user's subscription plan
    if not current_user.subscription_plan in ["pro", "agency"]:
        raise HTTPException(
            status_code=403,
            detail="SEO optimization requires Pro or Agency subscription"
        )
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Start timing
    start_time = time.time()
    
    try:
        # Perform optimization
        optimization_result = seo_optimizer.optimize_content(
            content=request.content,
            target_keywords=request.target_keywords,
            min_word_count=request.min_word_count,
            max_keyword_density=request.max_keyword_density
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create response
        response = OptimizationResponse(
            request_id=request_id,
            original_content=request.content,
            optimized_content=optimization_result["optimized_content"],
            seo_metrics={
                "score": optimization_result["score"],
                "suggestions": optimization_result["suggestions"],
                "keyword_metrics": optimization_result["metrics"].get("keyword_metrics", {}),
                "readability_metrics": optimization_result["metrics"].get("readability_metrics", {}),
                "structure_metrics": optimization_result["metrics"].get("structure_metrics", {}),
                "meta_tags": optimization_result["meta_tags"]
            },
            combined_score=optimization_result["score"],
            processing_time=processing_time,
            timestamp=datetime.utcnow()
        )
        
        # Save optimization result in background
        background_tasks.add_task(
            save_optimization_result,
            db=db,
            user_id=current_user.id,
            optimization_type="seo",
            request=request,
            response=response
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )

@router.post("/geo", response_model=OptimizationResponse)
async def optimize_geo(
    request: GEOOptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(requires_auth()),
    db: Session = Depends(get_db)
):
    """
    Optimize content for AI platforms
    """
    # Check user's subscription plan
    if not current_user.subscription_plan in ["pro", "agency"]:
        raise HTTPException(
            status_code=403,
            detail="GEO optimization requires Pro or Agency subscription"
        )
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Start timing
    start_time = time.time()
    
    try:
        # Perform optimization
        optimization_result = geo_optimizer.optimize_content(
            content=request.content,
            target_platforms=request.target_platforms,
            optimization_goals=request.optimization_goals
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create response
        response = OptimizationResponse(
            request_id=request_id,
            original_content=request.content,
            optimized_content=optimization_result["optimized_content"],
            geo_metrics={
                "score": optimization_result["score"],
                "suggestions": optimization_result["suggestions"],
                "context_clarity": optimization_result["metrics"].get("context_clarity", {}),
                "factual_consistency": optimization_result["metrics"].get("factual_consistency", {}),
                "voice_search": optimization_result["metrics"].get("voice_search", {}),
                "platform_specific": optimization_result["metrics"]
            },
            combined_score=optimization_result["score"],
            processing_time=processing_time,
            timestamp=datetime.utcnow()
        )
        
        # Save optimization result in background
        background_tasks.add_task(
            save_optimization_result,
            db=db,
            user_id=current_user.id,
            optimization_type="geo",
            request=request,
            response=response
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )

@router.post("/combined", response_model=OptimizationResponse)
async def optimize_combined(
    request: CombinedOptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(requires_auth()),
    db: Session = Depends(get_db)
):
    """
    Perform both SEO and GEO optimization
    """
    # Check user's subscription plan
    if not current_user.subscription_plan in ["pro", "agency"]:
        raise HTTPException(
            status_code=403,
            detail="Combined optimization requires Pro or Agency subscription"
        )
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    
    # Start timing
    start_time = time.time()
    
    try:
        # Perform SEO optimization
        seo_result = seo_optimizer.optimize_content(
            content=request.content,
            target_keywords=request.seo_settings.target_keywords,
            min_word_count=request.seo_settings.min_word_count,
            max_keyword_density=request.seo_settings.max_keyword_density
        )
        
        # Perform GEO optimization on SEO-optimized content
        geo_result = geo_optimizer.optimize_content(
            content=seo_result["optimized_content"],
            target_platforms=request.geo_settings.target_platforms,
            optimization_goals=request.geo_settings.optimization_goals
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Calculate combined score
        combined_score = (seo_result["score"] + geo_result["score"]) / 2
        
        # Create response
        response = OptimizationResponse(
            request_id=request_id,
            original_content=request.content,
            optimized_content=geo_result["optimized_content"],
            seo_metrics={
                "score": seo_result["score"],
                "suggestions": seo_result["suggestions"],
                "keyword_metrics": seo_result["metrics"].get("keyword_metrics", {}),
                "readability_metrics": seo_result["metrics"].get("readability_metrics", {}),
                "structure_metrics": seo_result["metrics"].get("structure_metrics", {}),
                "meta_tags": seo_result["meta_tags"]
            },
            geo_metrics={
                "score": geo_result["score"],
                "suggestions": geo_result["suggestions"],
                "context_clarity": geo_result["metrics"].get("context_clarity", {}),
                "factual_consistency": geo_result["metrics"].get("factual_consistency", {}),
                "voice_search": geo_result["metrics"].get("voice_search", {}),
                "platform_specific": geo_result["metrics"]
            },
            combined_score=combined_score,
            processing_time=processing_time,
            timestamp=datetime.utcnow()
        )
        
        # Save optimization result in background
        background_tasks.add_task(
            save_optimization_result,
            db=db,
            user_id=current_user.id,
            optimization_type="combined",
            request=request,
            response=response
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )

@router.get("/history", response_model=OptimizationHistory)
async def get_optimization_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(requires_auth()),
    db: Session = Depends(get_db)
):
    """
    Get user's optimization history
    """
    # Get total count
    total = db.query(Optimization).filter(
        Optimization.user_id == current_user.id
    ).count()
    
    # Get optimizations
    optimizations = db.query(Optimization).filter(
        Optimization.user_id == current_user.id
    ).order_by(
        Optimization.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return OptimizationHistory(
        total_optimizations=total,
        optimizations=[
            OptimizationResponse(
                request_id=str(opt.id),
                original_content=opt.original_content,
                optimized_content=opt.optimized_content,
                seo_metrics=opt.metrics.get("seo_metrics"),
                geo_metrics=opt.metrics.get("geo_metrics"),
                combined_score=opt.metrics.get("combined_score", 0.0),
                processing_time=opt.metrics.get("processing_time", 0.0),
                timestamp=opt.created_at
            ) for opt in optimizations
        ]
    )

async def save_optimization_result(
    db: Session,
    user_id: int,
    optimization_type: str,
    request: dict,
    response: OptimizationResponse
):
    """Save optimization result to database"""
    try:
        # Create optimization record
        optimization = Optimization(
            user_id=user_id,
            content_type=request.content_type,
            original_content=response.original_content,
            optimized_content=response.optimized_content,
            seo_score=response.seo_metrics.score if response.seo_metrics else None,
            geo_score=response.geo_metrics.score if response.geo_metrics else None,
            metrics={
                "seo_metrics": response.seo_metrics.dict() if response.seo_metrics else None,
                "geo_metrics": response.geo_metrics.dict() if response.geo_metrics else None,
                "combined_score": response.combined_score,
                "processing_time": response.processing_time
            }
        )
        db.add(optimization)
        db.commit()
        db.refresh(optimization)
        
        # Create suggestion records
        suggestions = []
        if response.seo_metrics:
            suggestions.extend([
                OptimizationSuggestion(
                    optimization_id=optimization.id,
                    category="seo",
                    suggestion=suggestion
                )
                for suggestion in response.seo_metrics.suggestions
            ])
        
        if response.geo_metrics:
            suggestions.extend([
                OptimizationSuggestion(
                    optimization_id=optimization.id,
                    category="geo",
                    suggestion=suggestion
                )
                for suggestion in response.geo_metrics.suggestions
            ])
        
        if suggestions:
            db.bulk_save_objects(suggestions)
            db.commit()
    
    except Exception as e:
        db.rollback()
        print(f"Error saving optimization result: {str(e)}")
        # Log error but don't raise exception since this is a background task 