from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Union
from datetime import datetime

class ContentBase(BaseModel):
    """Base model for content"""
    content: str = Field(..., description="The content to optimize")
    content_type: str = Field("text", description="Type of content (text, url, file)")
    language: str = Field("en", description="Content language code")

class SEOOptimizationRequest(ContentBase):
    """Request model for SEO optimization"""
    target_keywords: Optional[List[str]] = Field(
        None,
        description="Target keywords for optimization"
    )
    min_word_count: int = Field(
        300,
        description="Minimum word count for content"
    )
    max_keyword_density: float = Field(
        0.03,
        description="Maximum keyword density (0-1)"
    )
    optimization_goals: List[str] = Field(
        ["keyword_optimization", "technical_seo", "content_structure"],
        description="Optimization goals"
    )

class GEOOptimizationRequest(ContentBase):
    """Request model for GEO optimization"""
    target_platforms: List[str] = Field(
        ["chatgpt", "claude", "voice"],
        description="Target AI platforms"
    )
    optimization_goals: List[str] = Field(
        ["context", "factual", "voice_search"],
        description="Optimization goals"
    )

class CombinedOptimizationRequest(ContentBase):
    """Request model for combined optimization"""
    seo_settings: SEOOptimizationRequest
    geo_settings: GEOOptimizationRequest

class MetricsBase(BaseModel):
    """Base model for optimization metrics"""
    score: float = Field(..., description="Overall optimization score (0-100)")
    suggestions: List[str] = Field(
        ...,
        description="List of optimization suggestions"
    )

class SEOMetrics(MetricsBase):
    """Model for SEO optimization metrics"""
    keyword_metrics: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Keyword-specific metrics"
    )
    readability_metrics: Dict[str, float] = Field(
        ...,
        description="Readability metrics"
    )
    structure_metrics: Dict[str, int] = Field(
        ...,
        description="Content structure metrics"
    )
    meta_tags: Dict[str, str] = Field(
        ...,
        description="Generated meta tags"
    )

class GEOMetrics(MetricsBase):
    """Model for GEO optimization metrics"""
    context_clarity: Dict[str, float] = Field(
        ...,
        description="Context clarity metrics"
    )
    factual_consistency: Dict[str, int] = Field(
        ...,
        description="Factual consistency metrics"
    )
    voice_search: Dict[str, Union[int, float]] = Field(
        ...,
        description="Voice search optimization metrics"
    )
    platform_specific: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Platform-specific metrics"
    )

class OptimizationResponse(BaseModel):
    """Response model for optimization results"""
    request_id: str = Field(..., description="Unique request identifier")
    original_content: str = Field(..., description="Original content")
    optimized_content: str = Field(..., description="Optimized content")
    seo_metrics: Optional[SEOMetrics] = Field(
        None,
        description="SEO optimization metrics"
    )
    geo_metrics: Optional[GEOMetrics] = Field(
        None,
        description="GEO optimization metrics"
    )
    combined_score: float = Field(
        ...,
        description="Combined optimization score"
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Optimization timestamp"
    )

class OptimizationHistory(BaseModel):
    """Model for optimization history"""
    total_optimizations: int = Field(..., description="Total number of optimizations")
    optimizations: List[OptimizationResponse] = Field(
        ...,
        description="List of optimization results"
    )

class URLContent(BaseModel):
    """Model for URL content extraction"""
    url: HttpUrl = Field(..., description="URL to extract content from")
    selectors: Optional[List[str]] = Field(
        None,
        description="CSS selectors for content extraction"
    )

class FileContent(BaseModel):
    """Model for file content"""
    filename: str = Field(..., description="Name of the file")
    content_type: str = Field(..., description="MIME type of the file")
    content: bytes = Field(..., description="File content in bytes")

class OptimizationTemplate(BaseModel):
    """Model for optimization templates"""
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    seo_settings: Optional[Dict] = Field(
        None,
        description="SEO optimization settings"
    )
    geo_settings: Optional[Dict] = Field(
        None,
        description="GEO optimization settings"
    )
    is_public: bool = Field(
        False,
        description="Whether the template is public"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Blog Post Optimization",
                "description": "Template for optimizing blog posts",
                "seo_settings": {
                    "min_word_count": 800,
                    "max_keyword_density": 0.02,
                    "optimization_goals": [
                        "keyword_optimization",
                        "content_structure"
                    ]
                },
                "geo_settings": {
                    "target_platforms": ["chatgpt", "claude"],
                    "optimization_goals": ["context", "factual"]
                },
                "is_public": True
            }
        } 