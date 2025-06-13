# Audio Processor API Reference

This document provides detailed information about the Audio Processor API.

## AudioProcessor

The main class for audio processing operations.

### Initialization

```python
from src.core.processors.audio_processor import AudioProcessor

processor = AudioProcessor()
```

### Methods

#### process_audio

Processes an audio file and returns metadata, features, and analysis results.

```python
async def process_audio(
    file_path: str,
    config: Optional[AudioProcessingConfig] = None
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the audio file
- `config` (AudioProcessingConfig, optional): Custom processing configuration

**Returns:**
- Dict containing:
  - `metadata`: Audio metadata
  - `features`: Extracted audio features
  - `segments`: Audio segments
  - `analysis`: Audio analysis results

**Raises:**
- `AudioProcessingError`: If processing fails

#### extract_metadata

Extracts metadata from an audio file.

```python
async def extract_metadata(file_path: str) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the audio file

**Returns:**
- Dict containing:
  - `duration`: Audio duration in seconds
  - `sample_rate`: Sample rate in Hz
  - `channels`: Number of channels
  - `bitrate`: Audio bitrate
  - `format`: File format
  - `codec`: Audio codec

**Raises:**
- `AudioProcessingError`: If metadata extraction fails

#### analyze_features

Extracts audio features from a file.

```python
async def analyze_features(
    file_path: str,
    feature_types: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the audio file
- `feature_types` (List[str], optional): Types of features to extract

**Returns:**
- Dict containing:
  - `spectrogram`: Spectrogram data
  - `mfcc`: MFCC features
  - `chroma`: Chroma features
  - `tempo`: Tempo estimation
  - `pitch`: Pitch analysis

**Raises:**
- `AudioProcessingError`: If feature extraction fails

#### detect_speech

Detects speech segments in audio.

```python
async def detect_speech(
    file_path: str,
    min_duration: float = 0.5
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_path` (str): Path to the audio file
- `min_duration` (float): Minimum duration for speech segments

**Returns:**
- List of dicts containing:
  - `start`: Start time in seconds
  - `end`: End time in seconds
  - `confidence`: Detection confidence
  - `type`: Segment type ("speech", "music", "noise")

**Raises:**
- `AudioProcessingError`: If speech detection fails

#### analyze_spectrum

Performs spectral analysis of audio.

```python
async def analyze_spectrum(
    file_path: str,
    window_size: int = 2048
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the audio file
- `window_size` (int): FFT window size

**Returns:**
- Dict containing:
  - `centroid`: Spectral centroid
  - `bandwidth`: Spectral bandwidth
  - `rolloff`: Spectral rolloff
  - `flatness`: Spectral flatness
  - `contrast`: Spectral contrast

**Raises:**
- `AudioProcessingError`: If spectral analysis fails

## AudioProcessingConfig

Configuration class for audio processing.

### Attributes

```python
class AudioProcessingConfig:
    sample_rate: int = 44100
    channels: int = 2
    bitrate: str = "192k"
    format: str = "wav"
    segment_length: float = 30.0
    feature_types: List[str] = ["mfcc", "spectrogram", "chroma"]
    detect_speech: bool = True
```

### Usage

```python
from src.core.config import AudioProcessingConfig

config = AudioProcessingConfig(
    sample_rate=48000,
    channels=2,
    bitrate="256k",
    format="wav",
    segment_length=60.0,
    feature_types=["mfcc", "spectrogram"],
    detect_speech=True
)

processor = AudioProcessor()
result = await processor.process_audio("input.wav", config=config)
```

## Exceptions

### AudioProcessingError

Exception raised when audio processing fails.

```python
class AudioProcessingError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Basic Audio Processing

```python
from src.core.processors.audio_processor import AudioProcessor

async def process_audio_file(file_path: str):
    processor = AudioProcessor()
    
    try:
        # Process audio
        result = await processor.process_audio(file_path)
        
        # Access results
        metadata = result["metadata"]
        features = result["features"]
        segments = result["segments"]
        
        return result
    except AudioProcessingError as e:
        print(f"Error processing audio: {e}")
        return None
```

### Custom Configuration

```python
from src.core.config import AudioProcessingConfig
from src.core.processors.audio_processor import AudioProcessor

async def process_audio_with_config(file_path: str):
    # Create custom configuration
    config = AudioProcessingConfig(
        sample_rate=48000,
        channels=2,
        bitrate="256k",
        format="wav",
        segment_length=60.0,
        feature_types=["mfcc", "spectrogram"],
        detect_speech=True
    )
    
    processor = AudioProcessor()
    result = await processor.process_audio(file_path, config=config)
    return result
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from src.core.processors.audio_processor import AudioProcessor

async def process_audio_directory(directory: str):
    processor = AudioProcessor()
    audio_files = Path(directory).glob("*.wav")
    
    tasks = [
        processor.process_audio(str(file))
        for file in audio_files
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

### Streaming Processing

```python
from src.core.processors.audio_processor import AudioProcessor

async def process_audio_stream(file_path: str, chunk_size: int = 1024):
    processor = AudioProcessor()
    
    async for chunk in processor.stream_audio(file_path, chunk_size):
        # Process each chunk
        features = await processor.analyze_features(chunk)
        # Handle features
``` 