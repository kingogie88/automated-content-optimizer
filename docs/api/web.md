# Web Interface API Reference

This document provides detailed information about the Web Interface API.

## WebInterface

The main class for web interface operations.

### Initialization

```python
from src.web.interface import WebInterface

interface = WebInterface()
```

### Methods

#### start_server

Starts the web server.

```python
async def start_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    debug: bool = False
) -> None
```

**Parameters:**
- `host` (str): Server host address
- `port` (int): Server port number
- `debug` (bool): Enable debug mode

**Raises:**
- `WebInterfaceError`: If server startup fails

#### stop_server

Stops the web server.

```python
async def stop_server() -> None
```

**Raises:**
- `WebInterfaceError`: If server shutdown fails

#### get_status

Gets the current server status.

```python
async def get_status() -> Dict[str, Any]
```

**Returns:**
- Dict containing:
  - `running`: Server running status
  - `host`: Server host
  - `port`: Server port
  - `connections`: Active connections
  - `uptime`: Server uptime

**Raises:**
- `WebInterfaceError`: If status retrieval fails

## API Endpoints

### Content Processing

#### POST /api/process

Processes content and returns results.

**Request Body:**
```json
{
    "file_path": "string",
    "config": {
        "target_quality": "number",
        "optimization_rules": {
            "video": {
                "min_resolution": [1280, 720],
                "max_bitrate": "5M",
                "target_fps": 30
            },
            "audio": {
                "sample_rate": 44100,
                "channels": 2,
                "bitrate": "192k"
            }
        }
    }
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "score": {
            "video": 0.8,
            "audio": 0.9,
            "overall": 0.85
        },
        "recommendations": [
            {
                "category": "video",
                "suggestion": "Increase bitrate",
                "priority": "high",
                "impact": 0.1
            }
        ],
        "optimized_content": "path/to/optimized.mp4"
    }
}
```

#### GET /api/status

Gets the current processing status.

**Response:**
```json
{
    "status": "success",
    "data": {
        "running": true,
        "host": "0.0.0.0",
        "port": 8000,
        "connections": 5,
        "uptime": "2h 30m"
    }
}
```

### Content Analysis

#### POST /api/analyze

Analyzes content and returns analysis results.

**Request Body:**
```json
{
    "file_path": "string",
    "analysis_type": "string"
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "metadata": {
            "duration": 120,
            "resolution": [1920, 1080],
            "fps": 30
        },
        "features": {
            "video": {
                "motion": 0.7,
                "scene_changes": 15
            },
            "audio": {
                "speech_ratio": 0.8,
                "music_ratio": 0.2
            }
        }
    }
}
```

## WebInterfaceConfig

Configuration class for web interface.

### Attributes

```python
class WebInterfaceConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = ["*"]
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: List[str] = ["mp4", "wav", "mp3"]
    enable_swagger: bool = True
    enable_metrics: bool = True
```

### Usage

```python
from src.web.config import WebInterfaceConfig

config = WebInterfaceConfig(
    host="0.0.0.0",
    port=8000,
    debug=True,
    cors_origins=["http://localhost:3000"],
    max_upload_size=200 * 1024 * 1024,  # 200MB
    allowed_extensions=["mp4", "wav", "mp3"],
    enable_swagger=True,
    enable_metrics=True
)

interface = WebInterface()
await interface.start_server(config=config)
```

## Exceptions

### WebInterfaceError

Exception raised when web interface operations fail.

```python
class WebInterfaceError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
```

## Examples

### Basic Server Setup

```python
from src.web.interface import WebInterface

async def start_web_server():
    interface = WebInterface()
    
    try:
        await interface.start_server(
            host="0.0.0.0",
            port=8000,
            debug=True
        )
    except WebInterfaceError as e:
        print(f"Error starting server: {e}")
        return None
```

### Custom Configuration

```python
from src.web.config import WebInterfaceConfig
from src.web.interface import WebInterface

async def start_web_server_with_config():
    # Create custom configuration
    config = WebInterfaceConfig(
        host="0.0.0.0",
        port=8000,
        debug=True,
        cors_origins=["http://localhost:3000"],
        max_upload_size=200 * 1024 * 1024,
        allowed_extensions=["mp4", "wav", "mp3"],
        enable_swagger=True,
        enable_metrics=True
    )
    
    interface = WebInterface()
    await interface.start_server(config=config)
```

### API Client

```python
import aiohttp
from src.web.interface import WebInterface

async def process_content(file_path: str):
    async with aiohttp.ClientSession() as session:
        # Process content
        async with session.post(
            "http://localhost:8000/api/process",
            json={
                "file_path": file_path,
                "config": {
                    "target_quality": 0.8,
                    "optimization_rules": {
                        "video": {
                            "min_resolution": [1280, 720],
                            "max_bitrate": "5M",
                            "target_fps": 30
                        },
                        "audio": {
                            "sample_rate": 44100,
                            "channels": 2,
                            "bitrate": "192k"
                        }
                    }
                }
            }
        ) as response:
            result = await response.json()
            return result
```

### Status Monitoring

```python
import aiohttp
from src.web.interface import WebInterface

async def monitor_server_status():
    async with aiohttp.ClientSession() as session:
        # Get server status
        async with session.get("http://localhost:8000/api/status") as response:
            status = await response.json()
            
            if status["data"]["running"]:
                print(f"Server is running on {status['data']['host']}:{status['data']['port']}")
                print(f"Active connections: {status['data']['connections']}")
                print(f"Uptime: {status['data']['uptime']}")
            else:
                print("Server is not running")
``` 