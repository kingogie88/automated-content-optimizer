# Video Processing Guide

This guide covers the video processing capabilities of the Automated Content Optimizer.

## Features

- Metadata extraction
- Key frame detection
- Audio track separation
- Format validation
- Hardware-accelerated processing

## Basic Usage

### Processing a Video

```python
from src.core.processors.video_processor import VideoProcessor

# Initialize the processor
processor = VideoProcessor()

# Process a video file
result = await processor.process_video("input.mp4")

# Access the results
metadata = result["metadata"]
key_frames = result["key_frames"]
audio_path = result["audio_path"]
```

### Extracting Metadata

```python
# Get video metadata
metadata = await processor.extract_metadata("input.mp4")

# Access specific metadata
duration = metadata["duration"]
resolution = metadata["resolution"]
fps = metadata["fps"]
codec = metadata["codec"]
```

### Detecting Key Frames

```python
# Extract key frames
key_frames = await processor.detect_key_frames("input.mp4")

# Save key frames
for i, frame in enumerate(key_frames):
    frame.save(f"key_frame_{i}.jpg")
```

## Advanced Usage

### Custom Processing Options

```python
from src.core.config import VideoProcessingConfig

# Create custom configuration
config = VideoProcessingConfig(
    key_frame_threshold=0.5,
    max_key_frames=10,
    extract_audio=True,
    hardware_acceleration=True
)

# Process with custom configuration
result = await processor.process_video("input.mp4", config=config)
```

### Batch Processing

```python
import asyncio
from pathlib import Path

async def process_directory(directory: str):
    processor = VideoProcessor()
    video_files = Path(directory).glob("*.mp4")
    
    tasks = [
        processor.process_video(str(video_file))
        for video_file in video_files
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Process all videos in a directory
results = await process_directory("videos/")
```

## Performance Optimization

### Hardware Acceleration

```python
# Enable hardware acceleration
processor = VideoProcessor(use_hardware_acceleration=True)

# Process video with hardware acceleration
result = await processor.process_video("input.mp4")
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

async def process_videos_parallel(video_files: list[str]):
    processor = VideoProcessor()
    
    with ThreadPoolExecutor() as executor:
        tasks = [
            processor.process_video(video_file)
            for video_file in video_files
        ]
        results = await asyncio.gather(*tasks)
    
    return results
```

## Error Handling

```python
from src.core.exceptions import VideoProcessingError

try:
    result = await processor.process_video("input.mp4")
except VideoProcessingError as e:
    print(f"Error processing video: {e}")
    # Handle the error appropriately
```

## Best Practices

1. **File Validation**
   - Always validate input files before processing
   - Check file size and format
   - Ensure sufficient disk space

2. **Resource Management**
   - Use context managers for file handling
   - Clean up temporary files
   - Monitor memory usage

3. **Error Handling**
   - Implement proper error handling
   - Log errors for debugging
   - Provide meaningful error messages

4. **Performance**
   - Use hardware acceleration when available
   - Implement parallel processing for batch operations
   - Optimize memory usage

## Troubleshooting

### Common Issues

1. **Memory Issues**
   - Reduce batch size
   - Use hardware acceleration
   - Implement streaming processing

2. **Performance Issues**
   - Check hardware acceleration settings
   - Optimize key frame detection parameters
   - Use parallel processing

3. **Format Issues**
   - Verify input file format
   - Check codec compatibility
   - Use supported file formats

### Getting Help

- Check the [API Reference](../api/video.md)
- Join our [community discussions](https://github.com/kingogie88/automated-content-optimizer/discussions)
- Create an issue on GitHub 