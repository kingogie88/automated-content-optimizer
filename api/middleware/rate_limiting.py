from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL)

class RateLimiter:
    """Rate limiting implementation using Redis"""
    
    def __init__(self, key_prefix: str, limit: int, window: int):
        """
        Initialize rate limiter
        
        Args:
            key_prefix: Prefix for Redis keys
            limit: Maximum number of requests
            window: Time window in seconds
        """
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window
    
    def _get_key(self, identifier: str) -> str:
        """Generate Redis key for rate limiting"""
        return f"{self.key_prefix}:{identifier}"
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed based on rate limits
        
        Args:
            identifier: Unique identifier (e.g., API key, IP address)
            
        Returns:
            bool: True if request is allowed, False otherwise
        """
        key = self._get_key(identifier)
        pipe = redis_client.pipeline()
        
        now = datetime.utcnow().timestamp()
        window_start = now - self.window
        
        # Remove old requests
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now): now})
        
        # Set key expiration
        pipe.expire(key, self.window)
        
        # Execute pipeline
        _, current_requests, _, _ = pipe.execute()
        
        return current_requests <= self.limit
    
    def get_remaining(self, identifier: str) -> dict:
        """
        Get remaining requests and reset time
        
        Args:
            identifier: Unique identifier
            
        Returns:
            dict: Remaining requests and reset time
        """
        key = self._get_key(identifier)
        pipe = redis_client.pipeline()
        
        now = datetime.utcnow().timestamp()
        window_start = now - self.window
        
        # Remove old requests
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        pipe.zcard(key)
        
        # Get oldest request timestamp
        pipe.zrange(key, 0, 0, withscores=True)
        
        # Execute pipeline
        _, current_requests, oldest = pipe.execute()
        
        remaining = max(0, self.limit - current_requests)
        
        reset_time = None
        if oldest:
            reset_time = datetime.fromtimestamp(oldest[0][1] + self.window)
        
        return {
            "remaining": remaining,
            "limit": self.limit,
            "reset": reset_time.isoformat() if reset_time else None
        }

class RateLimitMiddleware:
    """Middleware for API rate limiting"""
    
    def __init__(self):
        # Rate limits for different subscription plans
        self.rate_limits = {
            "free": RateLimiter("free", 60, 60),  # 60 requests per minute
            "pro": RateLimiter("pro", 300, 60),   # 300 requests per minute
            "agency": RateLimiter("agency", 1000, 60)  # 1000 requests per minute
        }
    
    async def __call__(self, request: Request, call_next):
        # Skip rate limiting for certain endpoints
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            # Use IP-based rate limiting for unauthenticated requests
            identifier = request.client.host
            rate_limiter = self.rate_limits["free"]
        else:
            # Get user's subscription plan
            user = request.state.user
            plan = user.subscription_plan if user else "free"
            rate_limiter = self.rate_limits.get(plan, self.rate_limits["free"])
            identifier = api_key
        
        if not rate_limiter.is_allowed(identifier):
            remaining = rate_limiter.get_remaining(identifier)
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "limit": remaining["limit"],
                    "remaining": remaining["remaining"],
                    "reset": remaining["reset"]
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        
        remaining = rate_limiter.get_remaining(identifier)
        response.headers["X-RateLimit-Limit"] = str(remaining["limit"])
        response.headers["X-RateLimit-Remaining"] = str(remaining["remaining"])
        if remaining["reset"]:
            response.headers["X-RateLimit-Reset"] = remaining["reset"]
        
        return response

def check_rate_limit(request: Request, limit: int, window: int):
    """
    Decorator for endpoint-specific rate limiting
    
    Args:
        request: FastAPI request object
        limit: Maximum number of requests
        window: Time window in seconds
    """
    api_key = request.headers.get("X-API-Key")
    identifier = api_key if api_key else request.client.host
    
    rate_limiter = RateLimiter(
        key_prefix=f"endpoint:{request.url.path}",
        limit=limit,
        window=window
    )
    
    if not rate_limiter.is_allowed(identifier):
        remaining = rate_limiter.get_remaining(identifier)
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded",
                "limit": remaining["limit"],
                "remaining": remaining["remaining"],
                "reset": remaining["reset"]
            }
        ) 