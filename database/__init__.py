from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./content_optimizer.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables and initial data"""
    from .models import Base, User, Role, SubscriptionPlan
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial data
    db = SessionLocal()
    
    try:
        # Create default roles if they don't exist
        default_roles = [
            {"name": "admin", "description": "Administrator"},
            {"name": "user", "description": "Regular user"},
            {"name": "agency", "description": "Agency user"}
        ]
        
        for role_data in default_roles:
            if not db.query(Role).filter_by(name=role_data["name"]).first():
                role = Role(**role_data)
                db.add(role)
        
        # Create default subscription plans if they don't exist
        default_plans = [
            {
                "name": "free",
                "price": 0.0,
                "monthly_limit": 10,
                "features": {
                    "seo_optimization": True,
                    "geo_optimization": False,
                    "api_access": False,
                    "white_label": False
                }
            },
            {
                "name": "pro",
                "price": 29.0,
                "monthly_limit": 500,
                "features": {
                    "seo_optimization": True,
                    "geo_optimization": True,
                    "api_access": True,
                    "white_label": False
                }
            },
            {
                "name": "agency",
                "price": 99.0,
                "monthly_limit": -1,  # Unlimited
                "features": {
                    "seo_optimization": True,
                    "geo_optimization": True,
                    "api_access": True,
                    "white_label": True
                }
            }
        ]
        
        for plan_data in default_plans:
            if not db.query(SubscriptionPlan).filter_by(name=plan_data["name"]).first():
                plan = SubscriptionPlan(**plan_data)
                db.add(plan)
        
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise e
    
    finally:
        db.close()

def get_user_by_email(db, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_api_key(db, api_key: str):
    """Get user by API key"""
    return db.query(User).filter(User.api_key == api_key).first()

def create_user(db, user_data: dict):
    """Create a new user"""
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db, user_id: int, user_data: dict):
    """Update user data"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user 