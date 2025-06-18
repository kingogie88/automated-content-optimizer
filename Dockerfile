# Build stage
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmagic1 \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements-dev.txt pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Test stage
FROM builder as test

# Copy source code and tests
COPY src/ ./src/
COPY tests/ ./tests/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p /app/uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Production stage
FROM builder as production

# Copy source code and config
COPY src/ ./src/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p /app/uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 7860

# Set up entrypoint
ENTRYPOINT ["python", "src/main.py"] 