from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from database import get_db, get_user_by_email, get_user_by_api_key
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="X-API-Key")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user_from_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    """Get current user from API key"""
    api_key_exception = HTTPException(
        status_code=401,
        detail="Invalid API key",
        headers={"WWW-Authenticate": "ApiKey"},
    )
    
    user = get_user_by_api_key(db, api_key)
    if user is None:
        raise api_key_exception
    
    return user

async def get_current_active_user(
    current_user = Security(get_current_user_from_token)
):
    """Check if the current user is active"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def check_api_key_rate_limit(user):
    """Check API key rate limits based on subscription plan"""
    # TODO: Implement rate limiting based on user's subscription plan
    return True

class RateLimitMiddleware:
    """Middleware for API rate limiting"""
    
    async def __call__(self, request, call_next):
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        
        if api_key:
            # Get user from API key
            db = next(get_db())
            user = get_user_by_api_key(db, api_key)
            
            if user and not check_api_key_rate_limit(user):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )
        
        response = await call_next(request)
        return response

class APIKeyMiddleware:
    """Middleware for API key authentication"""
    
    async def __call__(self, request, call_next):
        # Skip authentication for public endpoints
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/token"]:
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "API key required"}
            )
        
        # Validate API key
        db = next(get_db())
        user = get_user_by_api_key(db, api_key)
        
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key"}
            )
        
        # Add user to request state
        request.state.user = user
        
        response = await call_next(request)
        return response

def get_current_user(
    token: str = Depends(oauth2_scheme),
    api_key: Optional[str] = Security(api_key_header),
    db: Session = Depends(get_db)
):
    """Get current user from either JWT token or API key"""
    if api_key:
        user = get_user_by_api_key(db, api_key)
        if user:
            return user
    
    return get_current_user_from_token(token, db)

def requires_auth(roles: Optional[list] = None):
    """Decorator for role-based authentication"""
    async def wrapper(current_user = Security(get_current_user)):
        if roles:
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=403,
                    detail="Not enough permissions"
                )
        return current_user
    return wrapper 