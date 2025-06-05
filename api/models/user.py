from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Dict, Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    """Base model for user data"""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="Username")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    """Model for user creation"""
    password: str = Field(
        ...,
        description="User's password",
        min_length=8
    )
    
    @validator('password')
    def password_strength(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', v):
            raise ValueError(
                'Password must be at least 8 characters long and contain both letters and numbers'
            )
        return v

class UserUpdate(BaseModel):
    """Model for user updates"""
    email: Optional[EmailStr] = Field(None, description="New email address")
    password: Optional[str] = Field(None, description="New password")
    subscription_plan: Optional[str] = Field(None, description="Subscription plan")
    is_active: Optional[bool] = Field(None, description="Account status")

class UserInDB(UserBase):
    """Model for user in database"""
    id: int
    password_hash: str
    subscription_plan: str = Field("free", description="User's subscription plan")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    is_active: bool = Field(True, description="Whether the user account is active")
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    """Model for user response"""
    id: int
    subscription_plan: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    """Model for authentication token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds

class TokenData(BaseModel):
    """Model for token payload"""
    sub: str  # subject (user email)
    exp: datetime
    scope: List[str] = []

class APIKey(BaseModel):
    """Model for API key"""
    key: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime]
    is_active: bool = True

class Role(BaseModel):
    """Model for user roles"""
    id: int
    name: str
    description: Optional[str]
    
    class Config:
        orm_mode = True

class SubscriptionPlanFeatures(BaseModel):
    """Model for subscription plan features"""
    seo_optimization: bool = True
    geo_optimization: bool = False
    api_access: bool = False
    white_label: bool = False
    max_optimizations: int = 10
    support_level: str = "basic"
    custom_templates: bool = False
    team_members: int = 1

class SubscriptionPlan(BaseModel):
    """Model for subscription plans"""
    id: int
    name: str
    price: float
    billing_interval: str = "monthly"
    features: SubscriptionPlanFeatures
    
    class Config:
        orm_mode = True

class UserActivity(BaseModel):
    """Model for user activity tracking"""
    user_id: int
    activity_type: str
    details: Dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str]
    user_agent: Optional[str]

class UserPreferences(BaseModel):
    """Model for user preferences"""
    user_id: int
    email_notifications: bool = True
    default_language: str = "en"
    default_optimization_settings: Dict = {}
    theme: str = "light"
    timezone: str = "UTC"

class TeamMember(BaseModel):
    """Model for team members (for agency accounts)"""
    user_id: int
    team_id: int
    role: str = "member"  # admin, member
    permissions: List[str] = []
    joined_at: datetime = Field(default_factory=datetime.utcnow)

class Team(BaseModel):
    """Model for teams"""
    id: int
    name: str
    owner_id: int
    members: List[TeamMember]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    settings: Dict = {}

class WhiteLabelSettings(BaseModel):
    """Model for white label settings"""
    company_name: str
    logo_url: Optional[str]
    primary_color: str = "#1f77b4"
    secondary_color: str = "#17a2b8"
    custom_domain: Optional[str]
    email_settings: Dict = {
        "from_name": "",
        "from_email": "",
        "reply_to": "",
        "footer_text": ""
    }
    
    @validator('primary_color', 'secondary_color')
    def validate_color(cls, v):
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
            raise ValueError('Invalid color hex code')
        return v 