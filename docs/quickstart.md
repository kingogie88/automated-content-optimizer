# Quick Start Guide

This guide will help you get started with the Automated Content Optimizer quickly.

## Basic Usage

### Video Processing

```python
from src.core.processors.video_processor import VideoProcessor

# Initialize the video processor
video_processor = VideoProcessor()

# Process a video file
result = await video_processor.process_video("path/to/video.mp4")

# Access the results
metadata = result["metadata"]
key_frames = result["key_frames"]
audio_path = result["audio_path"]
```

### Audio Processing

```python
from src.core.processors.audio_processor import AudioProcessor

# Initialize the audio processor
audio_processor = AudioProcessor()

# Process an audio file
result = await audio_processor.process_audio("path/to/audio.wav")

# Access the results
metadata = result["metadata"]
features = result["features"]
segments = result["segments"]
```

## Command Line Interface

The tool can also be used from the command line:

```bash
# Process a video file
python -m src.cli process-video path/to/video.mp4

# Process an audio file
python -m src.cli process-audio path/to/audio.wav

# Get help
python -m src.cli --help
```

## Web Interface

The tool includes a web interface for easy access:

1. Start the server:
   ```bash
   python -m src.web.app
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

3. Use the web interface to:
   - Upload and process media files
   - View processing results
   - Download optimized content

## Example Workflows

### Basic Video Optimization

```python
from src.core.processors.video_processor import VideoProcessor
from src.core.optimizers.video_optimizer import VideoOptimizer

# Initialize processors
video_processor = VideoProcessor()
video_optimizer = VideoOptimizer()

# Process and optimize video
video_result = await video_processor.process_video("input.mp4")
optimized_video = await video_optimizer.optimize(video_result)

# Save the optimized video
optimized_video.save("output.mp4")
```

### Audio Enhancement

```python
from src.core.processors.audio_processor import AudioProcessor
from src.core.optimizers.audio_optimizer import AudioOptimizer

# Initialize processors
audio_processor = AudioProcessor()
audio_optimizer = AudioOptimizer()

# Process and enhance audio
audio_result = await audio_processor.process_audio("input.wav")
enhanced_audio = await audio_optimizer.enhance(audio_result)

# Save the enhanced audio
enhanced_audio.save("output.wav")
```

## Next Steps

- Read the [Installation Guide](installation.md) for detailed setup instructions
- Check out the [API Reference](../api/video.md) for more advanced usage
- Explore the [User Guide](../user-guide/index.md) for detailed features
- Join our [community discussions](https://github.com/kingogie88/automated-content-optimizer/discussions) 