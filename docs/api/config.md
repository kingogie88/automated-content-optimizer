# Configuration System API Reference

This document provides detailed information about the Configuration System API.

## Configuration

The main class for configuration management.

### Initialization

```python
from src.core.config import Configuration

config = Configuration()
```

### Methods

#### load_config

Loads configuration from a file.

```python
async def load_config(
    config_path: str,
    validate: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `config_path` (str): Path to configuration file
- `validate` (bool): Whether to validate configuration

**Returns:**
- Dict containing configuration values

**Raises:**
- `ConfigurationError`: If loading fails

#### save_config

Saves configuration to a file.

```python
async def save_config(
    config: Dict[str, Any],
    config_path: str
) -> None
```

**Parameters:**
- `config` (Dict[str, Any]): Configuration to save
- `config_path` (str): Path to save configuration

**Raises:**
- `ConfigurationError`: If saving fails

#### validate_config

Validates configuration values.

```python
async def validate_config(
    config: Dict[str, Any]
) -> bool
```

**Parameters:**
- `config` (Dict[str, Any]): Configuration to validate

**Returns:**
- True if configuration is valid

**Raises:**
- `ConfigurationError`: If validation fails

## Configuration Classes

### BaseConfig

Base configuration class.

```python
class BaseConfig:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseConfig":
        return cls(**data)
```

### VideoProcessingConfig

Configuration for video processing.

```python
class VideoProcessingConfig(BaseConfig):
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30
    bitrate: str = "5M"
    codec: str = "h264"
    key_frame_interval: int = 30
    hardware_acceleration: bool = True
    parallel_processing: bool = True
```

### AudioProcessingConfig

Configuration for audio processing.

```python
class AudioProcessingConfig(BaseConfig):
    sample_rate: int = 44100
    channels: int = 2
    bitrate: str = "192k"
    format: str = "wav"
    segment_length: float = 30.0
    feature_types: List[str] = ["mfcc", "spectrogram", "chroma"]
    detect_speech: bool = True
```

### OptimizationConfig

Configuration for content optimization.

```python
class OptimizationConfig(BaseConfig):
    target_quality: float = 0.8
    optimization_rules: Dict[str, Dict[str, Any]] = {
        "video": {
            "min_resolution": (1280, 720),
            "max_bitrate": "5M",
            "target_fps": 30
        },
        "audio": {
            "sample_rate": 44100,
            "channels": 2,
            "bitrate": "192k"
        }
    }
    output_format: str = "mp4"
    preserve_metadata: bool = True
    parallel_processing: bool = True
```

### WebInterfaceConfig

Configuration for web interface.

```python
class WebInterfaceConfig(BaseConfig):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = ["*"]
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: List[str] = ["mp4", "wav", "mp3"]
    enable_swagger: bool = True
    enable_metrics: bool = True
```

## ConfigurationError

Exception raised when configuration operations fail.

```python
class ConfigurationError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Loading Configuration

```python
from src.core.config import Configuration

async def load_configuration(config_path: str):
    config = Configuration()
    
    try:
        config_data = await config.load_config(config_path)
        return config_data
    except ConfigurationError as e:
        print(f"Error loading configuration: {e}")
        return None
```

### Saving Configuration

```python
from src.core.config import Configuration

async def save_configuration(config_data: Dict[str, Any], config_path: str):
    config = Configuration()
    
    try:
        await config.save_config(config_data, config_path)
    except ConfigurationError as e:
        print(f"Error saving configuration: {e}")
        return None
```

### Using Configuration Classes

```python
from src.core.config import (
    VideoProcessingConfig,
    AudioProcessingConfig,
    OptimizationConfig
)

# Create video processing configuration
video_config = VideoProcessingConfig(
    resolution=(1280, 720),
    fps=24,
    bitrate="2M",
    codec="h264",
    key_frame_interval=60,
    hardware_acceleration=True,
    parallel_processing=True
)

# Create audio processing configuration
audio_config = AudioProcessingConfig(
    sample_rate=48000,
    channels=2,
    bitrate="256k",
    format="wav",
    segment_length=60.0,
    feature_types=["mfcc", "spectrogram"],
    detect_speech=True
)

# Create optimization configuration
optimization_config = OptimizationConfig(
    target_quality=0.9,
    optimization_rules={
        "video": {
            "min_resolution": (1920, 1080),
            "max_bitrate": "10M",
            "target_fps": 60
        },
        "audio": {
            "sample_rate": 48000,
            "channels": 2,
            "bitrate": "256k"
        }
    },
    output_format="mp4",
    preserve_metadata=True,
    parallel_processing=True
)
```

### Configuration Validation

```python
from src.core.config import Configuration

async def validate_configuration(config_data: Dict[str, Any]):
    config = Configuration()
    
    try:
        is_valid = await config.validate_config(config_data)
        if is_valid:
            print("Configuration is valid")
        else:
            print("Configuration is invalid")
    except ConfigurationError as e:
        print(f"Error validating configuration: {e}")
        return None
```

### Configuration File Format

```yaml
# config.yaml
video_processing:
  resolution: [1280, 720]
  fps: 24
  bitrate: 2M
  codec: h264
  key_frame_interval: 60
  hardware_acceleration: true
  parallel_processing: true

audio_processing:
  sample_rate: 48000
  channels: 2
  bitrate: 256k
  format: wav
  segment_length: 60.0
  feature_types:
    - mfcc
    - spectrogram
  detect_speech: true

optimization:
  target_quality: 0.9
  optimization_rules:
    video:
      min_resolution: [1920, 1080]
      max_bitrate: 10M
      target_fps: 60
    audio:
      sample_rate: 48000
      channels: 2
      bitrate: 256k
  output_format: mp4
  preserve_metadata: true
  parallel_processing: true

web_interface:
  host: 0.0.0.0
  port: 8000
  debug: true
  cors_origins:
    - http://localhost:3000
  max_upload_size: 200MB
  allowed_extensions:
    - mp4
    - wav
    - mp3
  enable_swagger: true
  enable_metrics: true
```

### Environment Variables

```python
from src.core.config import Configuration
import os

async def load_config_from_env():
    config = Configuration()
    
    # Load configuration from environment variables
    config_data = {
        "video_processing": {
            "resolution": os.getenv("VIDEO_RESOLUTION", "1280,720").split(","),
            "fps": int(os.getenv("VIDEO_FPS", "24")),
            "bitrate": os.getenv("VIDEO_BITRATE", "2M"),
            "codec": os.getenv("VIDEO_CODEC", "h264"),
            "key_frame_interval": int(os.getenv("VIDEO_KEY_FRAME_INTERVAL", "60")),
            "hardware_acceleration": os.getenv("VIDEO_HARDWARE_ACCELERATION", "true").lower() == "true",
            "parallel_processing": os.getenv("VIDEO_PARALLEL_PROCESSING", "true").lower() == "true"
        },
        "audio_processing": {
            "sample_rate": int(os.getenv("AUDIO_SAMPLE_RATE", "48000")),
            "channels": int(os.getenv("AUDIO_CHANNELS", "2")),
            "bitrate": os.getenv("AUDIO_BITRATE", "256k"),
            "format": os.getenv("AUDIO_FORMAT", "wav"),
            "segment_length": float(os.getenv("AUDIO_SEGMENT_LENGTH", "60.0")),
            "feature_types": os.getenv("AUDIO_FEATURE_TYPES", "mfcc,spectrogram").split(","),
            "detect_speech": os.getenv("AUDIO_DETECT_SPEECH", "true").lower() == "true"
        }
    }
    
    return config_data 