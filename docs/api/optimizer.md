# Content Optimizer API Reference

This document provides detailed information about the Content Optimizer API.

## ContentOptimizer

The main class for content optimization operations.

### Initialization

```python
from src.core.optimizer import ContentOptimizer

optimizer = ContentOptimizer()
```

### Methods

#### optimize_content

Optimizes content and returns optimization results.

```python
async def optimize_content(
    file_path: str,
    config: Optional[OptimizationConfig] = None
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the content file
- `config` (OptimizationConfig, optional): Custom optimization configuration

**Returns:**
- Dict containing:
  - `score`: Content quality score
  - `recommendations`: Optimization recommendations
  - `optimized_content`: Path to optimized content
  - `analysis`: Content analysis results

**Raises:**
- `OptimizationError`: If optimization fails

#### score_content

Evaluates content quality and returns a score.

```python
async def score_content(file_path: str) -> Dict[str, float]
```

**Parameters:**
- `file_path` (str): Path to the content file

**Returns:**
- Dict containing:
  - `video`: Video quality score (0.0 to 1.0)
  - `audio`: Audio quality score (0.0 to 1.0)
  - `overall`: Overall quality score (0.0 to 1.0)

**Raises:**
- `OptimizationError`: If scoring fails

#### get_recommendations

Generates optimization recommendations.

```python
async def get_recommendations(
    file_path: str,
    priority: str = "all"
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_path` (str): Path to the content file
- `priority` (str): Priority level ("high", "medium", "low", "all")

**Returns:**
- List of dicts containing:
  - `category`: Recommendation category
  - `suggestion`: Optimization suggestion
  - `priority`: Priority level
  - `impact`: Expected impact score

**Raises:**
- `OptimizationError`: If recommendation generation fails

#### optimize_video

Optimizes video quality.

```python
async def optimize_video(
    file_path: str,
    target_quality: float = 0.8
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the video file
- `target_quality` (float): Target quality score (0.0 to 1.0)

**Returns:**
- Dict containing:
  - `resolution`: Optimized resolution
  - `bitrate`: Optimized bitrate
  - `fps`: Optimized frame rate
  - `output_path`: Path to optimized video

**Raises:**
- `OptimizationError`: If video optimization fails

#### optimize_audio

Optimizes audio quality.

```python
async def optimize_audio(
    file_path: str,
    target_quality: float = 0.8
) -> Dict[str, Any]
```

**Parameters:**
- `file_path` (str): Path to the audio file
- `target_quality` (float): Target quality score (0.0 to 1.0)

**Returns:**
- Dict containing:
  - `sample_rate`: Optimized sample rate
  - `channels`: Optimized channel count
  - `bitrate`: Optimized bitrate
  - `output_path`: Path to optimized audio

**Raises:**
- `OptimizationError`: If audio optimization fails

## OptimizationConfig

Configuration class for content optimization.

### Attributes

```python
class OptimizationConfig:
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

### Usage

```python
from src.core.config import OptimizationConfig

config = OptimizationConfig(
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

optimizer = ContentOptimizer()
result = await optimizer.optimize_content("input.mp4", config=config)
```

## Exceptions

### OptimizationError

Exception raised when content optimization fails.

```python
class OptimizationError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Basic Content Optimization

```python
from src.core.optimizer import ContentOptimizer

async def optimize_content_file(file_path: str):
    optimizer = ContentOptimizer()
    
    try:
        # Optimize content
        result = await optimizer.optimize_content(file_path)
        
        # Access results
        score = result["score"]
        recommendations = result["recommendations"]
        optimized_content = result["optimized_content"]
        
        return result
    except OptimizationError as e:
        print(f"Error optimizing content: {e}")
        return None
```

### Custom Configuration

```python
from src.core.config import OptimizationConfig
from src.core.optimizer import ContentOptimizer

async def optimize_content_with_config(file_path: str):
    # Create custom configuration
    config = OptimizationConfig(
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
    
    optimizer = ContentOptimizer()
    result = await optimizer.optimize_content(file_path, config=config)
    return result
```

### Batch Optimization

```python
import asyncio
from pathlib import Path
from src.core.optimizer import ContentOptimizer

async def optimize_content_directory(directory: str):
    optimizer = ContentOptimizer()
    content_files = Path(directory).glob("*.mp4")
    
    tasks = [
        optimizer.optimize_content(str(file))
        for file in content_files
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

### Quality Scoring

```python
from src.core.optimizer import ContentOptimizer

async def evaluate_content_quality(file_path: str):
    optimizer = ContentOptimizer()
    
    try:
        # Get content score
        score = await optimizer.score_content(file_path)
        
        # Get recommendations
        recommendations = await optimizer.get_recommendations(
            file_path,
            priority="high"
        )
        
        return {
            "score": score,
            "recommendations": recommendations
        }
    except OptimizationError as e:
        print(f"Error evaluating content: {e}")
        return None
``` 