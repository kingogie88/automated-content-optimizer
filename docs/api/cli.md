# Command Line Interface API Reference

This document provides detailed information about the Command Line Interface API.

## CLI

The main class for command line interface operations.

### Initialization

```python
from src.cli.interface import CLI

cli = CLI()
```

### Methods

#### process_content

Processes content from the command line.

```python
async def process_content(
    file_path: str,
    config_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> None
```

**Parameters:**
- `file_path` (str): Path to the content file
- `config_path` (str, optional): Path to configuration file
- `output_path` (str, optional): Path to save output

**Raises:**
- `CLIError`: If processing fails

#### analyze_content

Analyzes content from the command line.

```python
async def analyze_content(
    file_path: str,
    analysis_type: str = "full"
) -> None
```

**Parameters:**
- `file_path` (str): Path to the content file
- `analysis_type` (str): Type of analysis ("basic", "full", "custom")

**Raises:**
- `CLIError`: If analysis fails

#### optimize_content

Optimizes content from the command line.

```python
async def optimize_content(
    file_path: str,
    target_quality: float = 0.8,
    output_path: Optional[str] = None
) -> None
```

**Parameters:**
- `file_path` (str): Path to the content file
- `target_quality` (float): Target quality score (0.0 to 1.0)
- `output_path` (str, optional): Path to save optimized content

**Raises:**
- `CLIError`: If optimization fails

## Command Line Arguments

### Process Command

```bash
python -m src.cli process [OPTIONS] FILE_PATH
```

**Options:**
- `--config, -c`: Path to configuration file
- `--output, -o`: Path to save output
- `--verbose, -v`: Enable verbose output
- `--debug, -d`: Enable debug mode

### Analyze Command

```bash
python -m src.cli analyze [OPTIONS] FILE_PATH
```

**Options:**
- `--type, -t`: Analysis type ("basic", "full", "custom")
- `--output, -o`: Path to save analysis results
- `--verbose, -v`: Enable verbose output
- `--debug, -d`: Enable debug mode

### Optimize Command

```bash
python -m src.cli optimize [OPTIONS] FILE_PATH
```

**Options:**
- `--quality, -q`: Target quality score (0.0 to 1.0)
- `--output, -o`: Path to save optimized content
- `--verbose, -v`: Enable verbose output
- `--debug, -d`: Enable debug mode

## Configuration File

### Format

```yaml
# config.yaml
target_quality: 0.8
optimization_rules:
  video:
    min_resolution: [1280, 720]
    max_bitrate: 5M
    target_fps: 30
  audio:
    sample_rate: 44100
    channels: 2
    bitrate: 192k
output_format: mp4
preserve_metadata: true
parallel_processing: true
```

### Usage

```bash
python -m src.cli process --config config.yaml input.mp4
```

## CLIError

Exception raised when CLI operations fail.

```python
class CLIError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Basic Processing

```python
from src.cli.interface import CLI

async def process_file(file_path: str):
    cli = CLI()
    
    try:
        await cli.process_content(file_path)
    except CLIError as e:
        print(f"Error processing file: {e}")
        return None
```

### Custom Configuration

```python
from src.cli.interface import CLI

async def process_with_config(file_path: str, config_path: str):
    cli = CLI()
    
    try:
        await cli.process_content(
            file_path,
            config_path=config_path,
            output_path="output.mp4"
        )
    except CLIError as e:
        print(f"Error processing file: {e}")
        return None
```

### Content Analysis

```python
from src.cli.interface import CLI

async def analyze_file(file_path: str):
    cli = CLI()
    
    try:
        await cli.analyze_content(
            file_path,
            analysis_type="full"
        )
    except CLIError as e:
        print(f"Error analyzing file: {e}")
        return None
```

### Content Optimization

```python
from src.cli.interface import CLI

async def optimize_file(file_path: str):
    cli = CLI()
    
    try:
        await cli.optimize_content(
            file_path,
            target_quality=0.9,
            output_path="optimized.mp4"
        )
    except CLIError as e:
        print(f"Error optimizing file: {e}")
        return None
```

### Command Line Usage

```bash
# Process content
python -m src.cli process --config config.yaml input.mp4

# Analyze content
python -m src.cli analyze --type full input.mp4

# Optimize content
python -m src.cli optimize --quality 0.9 input.mp4

# Enable verbose output
python -m src.cli process -v input.mp4

# Enable debug mode
python -m src.cli process -d input.mp4
```

### Batch Processing

```bash
# Process all files in a directory
for file in *.mp4; do
    python -m src.cli process "$file"
done

# Process with custom output
for file in *.mp4; do
    output="${file%.*}_optimized.mp4"
    python -m src.cli process -o "$output" "$file"
done
```

### Error Handling

```python
from src.cli.interface import CLI
from src.cli.exceptions import CLIError

async def process_with_error_handling(file_path: str):
    cli = CLI()
    
    try:
        await cli.process_content(file_path)
    except CLIError as e:
        if e.error_code == 1:
            print("File not found")
        elif e.error_code == 2:
            print("Invalid configuration")
        else:
            print(f"Unknown error: {e}")
        return None
``` 