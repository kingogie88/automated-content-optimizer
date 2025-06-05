# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Create entrypoint script
RUN echo '#!/bin/bash\n\
uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0\
' > /app/entrypoint.sh \
&& chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 