from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProcessingConfig:
    # Image processing settings
    image_max_size: tuple = (1024, 1024)
    supported_image_formats: list = ("jpg", "jpeg", "png", "webp")
    image_quality: int = 85
    extract_image_text: bool = True
    
    # Video processing settings
    video_max_resolution: tuple = (1920, 1080)
    video_frame_rate: int = 30
    key_frame_interval: int = 60  # Extract a frame every 60 frames
    supported_video_formats: list = ("mp4", "mov", "avi")
    
    # Audio processing settings
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    supported_audio_formats: list = ("wav", "mp3", "ogg", "m4a")
    
    # Text processing settings
    max_text_length: int = 10000
    language_detection_confidence: float = 0.8
    supported_text_formats: list = ("txt", "md", "rst", "html")
    
    # Document processing settings
    supported_document_formats: list = ("pdf", "docx", "doc", "odt")
    extract_document_images: bool = True
    preserve_document_layout: bool = True
    
    # Model settings
    image_captioning_model: str = "Salesforce/blip-image-captioning-large"
    text_classification_model: str = "facebook/bart-large-mnli"
    whisper_model_size: str = "base"
    
    # Output settings
    output_format: str = "json"
    include_metadata: bool = True
    include_confidence_scores: bool = True
    
    # Cache settings
    enable_cache: bool = True
    cache_dir: Path = Path("cache")
    cache_ttl: int = 3600  # 1 hour
    
    # Performance settings
    batch_size: int = 16
    num_workers: int = 4
    use_gpu: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ProcessingConfig":
        """Create a ProcessingConfig instance from a dictionary."""
        return cls(**{
            k: v for k, v in config_dict.items()
            if k in cls.__dataclass_fields__
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the config to a dictionary."""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
    
    def validate(self) -> bool:
        """Validate the configuration settings."""
        try:
            assert all(x > 0 for x in self.image_max_size), "Invalid image dimensions"
            assert 0 < self.image_quality <= 100, "Invalid image quality"
            assert all(x > 0 for x in self.video_max_resolution), "Invalid video resolution"
            assert self.video_frame_rate > 0, "Invalid frame rate"
            assert self.key_frame_interval > 0, "Invalid key frame interval"
            assert self.audio_sample_rate > 0, "Invalid sample rate"
            assert self.audio_channels > 0, "Invalid audio channels"
            assert self.max_text_length > 0, "Invalid text length"
            assert 0 <= self.language_detection_confidence <= 1, "Invalid confidence threshold"
            assert self.batch_size > 0, "Invalid batch size"
            assert self.num_workers >= 0, "Invalid worker count"
            return True
        except AssertionError as e:
            print(f"Configuration validation failed: {str(e)}")
            return False
    
    def optimize_for_hardware(self) -> None:
        """Optimize settings based on available hardware."""
        try:
            import torch
            
            # Adjust GPU usage
            self.use_gpu = torch.cuda.is_available()
            
            if self.use_gpu:
                # Optimize batch size based on GPU memory
                gpu_mem = torch.cuda.get_device_properties(0).total_memory
                self.batch_size = min(self.batch_size, gpu_mem // (1024 * 1024 * 1024))  # Adjust based on GPU GB
            
            # Adjust workers based on CPU cores
            import multiprocessing
            cpu_count = multiprocessing.cpu_count()
            self.num_workers = min(self.num_workers, cpu_count - 1)
            
        except ImportError:
            print("PyTorch not available, using CPU settings")
            self.use_gpu = False
            self.num_workers = 2
            self.batch_size = 8 