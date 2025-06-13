# Video Processor API Reference

This document provides detailed information about the Video Processor API.

## VideoProcessor

The main class for video processing operations.

### Initialization

```python
from src.core.processors.video_processor import VideoProcessor

processor = VideoProcessor()
```

### Methods

#### process_video

Processes a video file and returns metadata, key frames, and other analysis results.

```python
async def process_video(
    file_path: str,
    config: Optional[VideoProcessingConfig] = None
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the video file
- `config` (VideoProcessingConfig, optional): Custom processing configuration

**Returns:**
- Dict containing:
  - `metadata`: Video metadata
  - `key_frames`: Detected key frames
  - `audio_track`: Extracted audio track
  - `analysis`: Video analysis results

**Raises:**
- `VideoProcessingError`: If processing fails

#### extract_metadata

Extracts metadata from a video file.

```python
async def extract_metadata(file_path: str) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the video file

**Returns:**
- Dict containing:
  - `duration`: Video duration in seconds
  - `resolution`: Tuple of (width, height)
  - `fps`: Frames per second
  - `bitrate`: Video bitrate
  - `codec`: Video codec
  - `format`: File format

**Raises:**
- `VideoProcessingError`: If metadata extraction fails

#### detect_key_frames

Detects key frames in a video.

```python
async def detect_key_frames(
    file_path: str,
    threshold: float = 0.5
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_path` (str): Path to the video file
- `threshold` (float): Detection threshold (0.0 to 1.0)

**Returns:**
- List of dicts containing:
  - `frame_number`: Frame number
  - `timestamp`: Timestamp in seconds
  - `confidence`: Detection confidence

**Raises:**
- `VideoProcessingError`: If key frame detection fails

#### extract_audio

Extracts audio track from a video file.

```python
async def extract_audio(
    file_path: str,
    output_path: Optional[str] = None
) -> str
```

**Parameters:**
- `file_path` (str): Path to the video file
- `output_path` (str, optional): Path to save the audio file

**Returns:**
- Path to the extracted audio file

**Raises:**
- `VideoProcessingError`: If audio extraction fails

#### analyze_video

Performs comprehensive video analysis.

```python
async def analyze_video(
    file_path: str,
    analysis_type: str = "full"
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the video file
- `analysis_type` (str): Type of analysis ("basic", "full", "custom")

**Returns:**
- Dict containing analysis results:
  - `motion`: Motion analysis
  - `scene_changes`: Scene change detection
  - `quality_metrics`: Video quality metrics
  - `content_analysis`: Content analysis results

**Raises:**
- `VideoProcessingError`: If analysis fails

## VideoProcessingConfig

Configuration class for video processing.

### Attributes

```python
class VideoProcessingConfig:
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30
    bitrate: str = "5M"
    codec: str = "h264"
    key_frame_interval: int = 30
    hardware_acceleration: bool = True
    parallel_processing: bool = True
```

### Usage

```python
from src.core.config import VideoProcessingConfig

config = VideoProcessingConfig(
    resolution=(1280, 720),
    fps=24,
    bitrate="2M",
    codec="h264",
    key_frame_interval=60,
    hardware_acceleration=True,
    parallel_processing=True
)

processor = VideoProcessor()
result = await processor.process_video("input.mp4", config=config)
```

## Exceptions

### VideoProcessingError

Exception raised when video processing fails.

```python
class VideoProcessingError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Basic Video Processing

```python
from src.core.processors.video_processor import VideoProcessor

async def process_video_file(file_path: str):
    processor = VideoProcessor()
    
    try:
        # Process video
        result = await processor.process_video(file_path)
        
        # Access results
        metadata = result["metadata"]
        key_frames = result["key_frames"]
        audio_track = result["audio_track"]
        
        return result
    except VideoProcessingError as e:
        print(f"Error processing video: {e}")
        return None
```

### Custom Configuration

```python
from src.core.config import VideoProcessingConfig
from src.core.processors.video_processor import VideoProcessor

async def process_video_with_config(file_path: str):
    # Create custom configuration
    config = VideoProcessingConfig(
        resolution=(1280, 720),
        fps=24,
        bitrate="2M",
        codec="h264",
        key_frame_interval=60,
        hardware_acceleration=True,
        parallel_processing=True
    )
    
    processor = VideoProcessor()
    result = await processor.process_video(file_path, config=config)
    return result
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from src.core.processors.video_processor import VideoProcessor

async def process_video_directory(directory: str):
    processor = VideoProcessor()
    video_files = Path(directory).glob("*.mp4")
    
    tasks = [
        processor.process_video(str(file))
        for file in video_files
    ]
    
    results = await asyncio.gather(*tasks)
    return results
``` 