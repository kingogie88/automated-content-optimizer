from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Set, Optional
import magic
import os
from pathlib import Path

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        
    async def check_rate_limit(self, request: Request) -> None:
        # Get client IP
        client_ip = request.client.host
        current_time = time.time()
        
        # Initialize or clean old requests
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)

class SecurityValidator:
    def __init__(self):
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_mime_types = {
            # Images
            'image/jpeg', 'image/png', 'image/gif', 'image/webp',
            # Documents
            'application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            # Audio
            'audio/mpeg', 'audio/wav', 'audio/ogg',
            # Video
            'video/mp4', 'video/mpeg', 'video/quicktime'
        }
        
    async def validate_file(self, file_path: str) -> None:
        """Validate file size and type."""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds maximum limit of {self.max_file_size // (1024*1024)}MB"
                )
            
            # Check file type
            mime_type = magic.from_file(file_path, mime=True)
            if mime_type not in self.allowed_mime_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {mime_type} not allowed"
                )
                
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

class SecurityMiddleware:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.validator = SecurityValidator()
        
    async def process_request(self, request: Request) -> None:
        """Process and validate incoming request."""
        # Check rate limit
        await self.rate_limiter.check_rate_limit(request)
        
        # Validate content length
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > self.validator.max_file_size:
            raise HTTPException(
                status_code=400,
                detail="Request body too large"
            )

async def security_middleware(request: Request, call_next):
    """FastAPI middleware for security checks."""
    try:
        security = SecurityMiddleware()
        await security.process_request(request)
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        ) 