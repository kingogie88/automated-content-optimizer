"""Configuration settings for multimodal content processing."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
import torch

class ProcessingConfig(BaseModel):
    """Configuration for multimodal content processing."""
    
    # Text processing settings
    text_languages: List[str] = Field(
        default=["en"],
        description="List of languages to process text in"
    )
    text_min_length: int = Field(
        default=10,
        description="Minimum text length to process"
    )
    
    # Image processing settings
    image_formats: List[str] = Field(
        default=["jpg", "jpeg", "png"],
        description="Supported image formats"
    )
    image_max_size: int = Field(
        default=1920,
        description="Maximum image dimension in pixels"
    )
    
    # Audio processing settings
    audio_formats: List[str] = Field(
        default=["mp3", "wav"],
        description="Supported audio formats"
    )
    audio_max_duration: int = Field(
        default=300,
        description="Maximum audio duration in seconds"
    )
    
    # Video processing settings
    video_formats: List[str] = Field(
        default=["mp4", "avi"],
        description="Supported video formats"
    )
    video_max_duration: int = Field(
        default=600,
        description="Maximum video duration in seconds"
    )
    
    # Model settings
    model_cache_dir: Optional[str] = Field(
        default=None,
        description="Directory to cache downloaded models"
    )
    
    # Processing settings
    batch_size: int = Field(
        default=32,
        description="Batch size for processing"
    )
    num_workers: int = Field(
        default=4,
        description="Number of worker processes"
    )

    # Hardware settings
    use_gpu: bool = Field(
        default=False,
        description="Whether to use GPU for processing"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())

    def optimize_for_hardware(self) -> None:
        """Optimize configuration based on available hardware."""
        # Check for GPU availability
        self.use_gpu = torch.cuda.is_available()
        
        # Adjust batch size based on GPU memory if available
        if self.use_gpu:
            gpu_memory = torch.cuda.get_device_properties(0).total_memory
            if gpu_memory < 4e9:  # Less than 4GB
                self.batch_size = 8
            elif gpu_memory < 8e9:  # Less than 8GB
                self.batch_size = 16
            else:
                self.batch_size = 32
        
        # Adjust number of workers based on CPU cores
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        self.num_workers = min(cpu_count, 8)  # Cap at 8 workers 