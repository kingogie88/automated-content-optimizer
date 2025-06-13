# Installation Guide

This guide will help you set up the Automated Content Optimizer on your system.

## Prerequisites

Before installing, ensure you have the following:

- Python 3.9 or higher
- FFmpeg (for video processing)
- libsndfile (for audio processing)

### System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg libsndfile1
```

#### macOS
```bash
brew install ffmpeg
brew install libsndfile
```

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add FFmpeg to your system PATH
3. Install libsndfile using [Chocolatey](https://chocolatey.org/):
   ```bash
   choco install libsndfile
   ```

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/kingogie88/automated-content-optimizer.git
   cd automated-content-optimizer
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   # Install production dependencies
   pip install -r requirements.txt
   
   # Install development dependencies (optional)
   pip install -r requirements-dev.txt
   ```

4. Verify installation:
   ```bash
   python -c "from src.core.processors.video_processor import VideoProcessor; from src.core.processors.audio_processor import AudioProcessor; print('Installation successful!')"
   ```

## Configuration

1. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

2. Update the configuration values in `.env` as needed.

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your system PATH
   - Try running `ffmpeg -version` to verify installation

2. **libsndfile not found**
   - Ensure libsndfile is installed
   - On Linux, you might need to install additional development packages:
     ```bash
     sudo apt-get install libsndfile1-dev
     ```

3. **Python version issues**
   - Ensure you're using Python 3.9 or higher
   - Check your Python version: `python --version`

4. **Virtual environment issues**
   - If you get permission errors, try:
     ```bash
     python -m venv .venv --clear
     ```
   - Make sure you're activating the virtual environment correctly

### Getting Help

If you encounter any issues not covered here:
1. Check the [GitHub Issues](https://github.com/kingogie88/automated-content-optimizer/issues)
2. Create a new issue with detailed information about your problem
3. Join our community discussions 