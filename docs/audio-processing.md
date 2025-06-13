# Audio Processing Guide

This guide covers the audio processing capabilities of the Automated Content Optimizer.

## Features

- Metadata extraction
- Audio segmentation
- Feature analysis
- Speech/music detection
- Format conversion

## Basic Usage

### Processing Audio

```python
from src.core.processors.audio_processor import AudioProcessor

# Initialize the processor
processor = AudioProcessor()

# Process an audio file
result = await processor.process_audio("input.wav")

# Access the results
metadata = result["metadata"]
features = result["features"]
segments = result["segments"]
```

### Extracting Metadata

```python
# Get audio metadata
metadata = await processor.extract_metadata("input.wav")

# Access specific metadata
duration = metadata["duration"]
sample_rate = metadata["sample_rate"]
channels = metadata["channels"]
format = metadata["format"]
```

### Analyzing Features

```python
# Extract audio features
features = await processor.analyze_features("input.wav")

# Access specific features
spectrogram = features["spectrogram"]
mfcc = features["mfcc"]
chroma = features["chroma"]
```

## Advanced Usage

### Custom Processing Options

```python
from src.core.config import AudioProcessingConfig

# Create custom configuration
config = AudioProcessingConfig(
    sample_rate=44100,
    segment_length=30,
    feature_types=["mfcc", "spectrogram"],
    detect_speech=True
)

# Process with custom configuration
result = await processor.process_audio("input.wav", config=config)
```

### Batch Processing

```python
import asyncio
from pathlib import Path

async def process_directory(directory: str):
    processor = AudioProcessor()
    audio_files = Path(directory).glob("*.wav")
    
    tasks = [
        processor.process_audio(str(audio_file))
        for audio_file in audio_files
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Process all audio files in a directory
results = await process_directory("audio/")
```

## Feature Analysis

### Spectral Analysis

```python
# Perform spectral analysis
spectral_features = await processor.analyze_spectrum("input.wav")

# Access spectral features
spectral_centroid = spectral_features["centroid"]
spectral_bandwidth = spectral_features["bandwidth"]
spectral_rolloff = spectral_features["rolloff"]
```

### Speech Detection

```python
# Detect speech segments
speech_segments = await processor.detect_speech("input.wav")

# Process speech segments
for segment in speech_segments:
    start_time = segment["start"]
    end_time = segment["end"]
    confidence = segment["confidence"]
```

## Performance Optimization

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

async def process_audio_parallel(audio_files: list[str]):
    processor = AudioProcessor()
    
    with ThreadPoolExecutor() as executor:
        tasks = [
            processor.process_audio(audio_file)
            for audio_file in audio_files
        ]
        results = await asyncio.gather(*tasks)
    
    return results
```

### Memory Management

```python
# Process audio in chunks
async def process_large_audio(file_path: str, chunk_size: int = 1024):
    processor = AudioProcessor()
    
    async for chunk in processor.stream_audio(file_path, chunk_size):
        # Process each chunk
        features = await processor.analyze_features(chunk)
        # Handle features
```

## Error Handling

```python
from src.core.exceptions import AudioProcessingError

try:
    result = await processor.process_audio("input.wav")
except AudioProcessingError as e:
    print(f"Error processing audio: {e}")
    # Handle the error appropriately
```

## Best Practices

1. **File Validation**
   - Validate input files before processing
   - Check file format and sample rate
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
   - Use parallel processing for batch operations
   - Implement streaming for large files
   - Optimize memory usage

## Troubleshooting

### Common Issues

1. **Memory Issues**
   - Reduce batch size
   - Use streaming processing
   - Implement chunk-based processing

2. **Performance Issues**
   - Use parallel processing
   - Optimize feature extraction parameters
   - Implement caching for repeated operations

3. **Format Issues**
   - Verify input file format
   - Check sample rate compatibility
   - Use supported file formats

### Getting Help

- Check the [API Reference](../api/audio.md)
- Join our [community discussions](https://github.com/kingogie88/automated-content-optimizer/discussions)
- Create an issue on GitHub 