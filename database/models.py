from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    subscription_plan = Column(String, default='free')
    api_key = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    optimizations = relationship('Optimization', back_populates='user')
    api_usage = relationship('APIUsage', back_populates='user')

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    
    # Relationships
    users = relationship('User', secondary=user_roles, back_populates='roles')

class Optimization(Base):
    __tablename__ = 'optimizations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content_type = Column(String, nullable=False)  # 'text', 'url', 'file'
    original_content = Column(String, nullable=False)
    optimized_content = Column(String, nullable=False)
    seo_score = Column(Float)
    geo_score = Column(Float)
    metrics = Column(JSON)  # Stores detailed optimization metrics
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='optimizations')
    suggestions = relationship('OptimizationSuggestion', back_populates='optimization')

class OptimizationSuggestion(Base):
    __tablename__ = 'optimization_suggestions'
    
    id = Column(Integer, primary_key=True)
    optimization_id = Column(Integer, ForeignKey('optimizations.id'))
    category = Column(String, nullable=False)  # 'seo', 'geo', 'voice', etc.
    suggestion = Column(String, nullable=False)
    implemented = Column(Integer, default=0)  # 0: not implemented, 1: implemented
    impact_score = Column(Float)  # Estimated impact of implementing the suggestion
    
    # Relationships
    optimization = relationship('Optimization', back_populates='suggestions')

class APIUsage(Base):
    __tablename__ = 'api_usage'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    endpoint = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Float)  # in milliseconds
    status_code = Column(Integer)
    error_message = Column(String)
    
    # Relationships
    user = relationship('User', back_populates='api_usage')

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    monthly_limit = Column(Integer)  # Number of optimizations allowed per month
    features = Column(JSON)  # List of features included in the plan
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class OptimizationTemplate(Base):
    __tablename__ = 'optimization_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    settings = Column(JSON)  # Optimization settings and parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    is_public = Column(Integer, default=0)  # 0: private, 1: public

class WhiteLabel(Base):
    __tablename__ = 'white_labels'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    company_name = Column(String, nullable=False)
    logo_url = Column(String)
    primary_color = Column(String)
    secondary_color = Column(String)
    custom_domain = Column(String)
    email_settings = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow) 