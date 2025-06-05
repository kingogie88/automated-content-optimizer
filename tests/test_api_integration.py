import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from api.main import app
from database import Base
from database.models import User, Role
from api.middleware.auth import create_access_token

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user(test_db):
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password",
        subscription_plan="pro"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(
        data={"sub": test_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_seo_optimization(client, auth_headers):
    """Test SEO optimization endpoint"""
    content = "Test content for SEO optimization"
    response = client.post(
        "/optimize/seo",
        headers=auth_headers,
        json={
            "content": content,
            "content_type": "text",
            "target_keywords": ["test", "seo"],
            "optimization_goals": ["keyword_optimization"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert "seo_metrics" in data
    assert data["original_content"] == content

def test_geo_optimization(client, auth_headers):
    """Test GEO optimization endpoint"""
    content = "Test content for AI optimization"
    response = client.post(
        "/optimize/geo",
        headers=auth_headers,
        json={
            "content": content,
            "content_type": "text",
            "target_platforms": ["chatgpt", "claude"],
            "optimization_goals": ["context", "factual"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert "geo_metrics" in data
    assert data["original_content"] == content

def test_combined_optimization(client, auth_headers):
    """Test combined optimization endpoint"""
    content = "Test content for combined optimization"
    response = client.post(
        "/optimize/combined",
        headers=auth_headers,
        json={
            "content": content,
            "content_type": "text",
            "seo_settings": {
                "target_keywords": ["test", "optimization"],
                "optimization_goals": ["keyword_optimization"]
            },
            "geo_settings": {
                "target_platforms": ["chatgpt"],
                "optimization_goals": ["context"]
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "seo_metrics" in data
    assert "geo_metrics" in data
    assert data["combined_score"] >= 0 and data["combined_score"] <= 100

def test_optimization_history(client, auth_headers, test_user):
    """Test optimization history endpoint"""
    # First create some optimization records
    content = "Test content"
    client.post(
        "/optimize/seo",
        headers=auth_headers,
        json={
            "content": content,
            "content_type": "text",
            "target_keywords": ["test"]
        }
    )
    
    response = client.get("/optimize/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_optimizations" in data
    assert "optimizations" in data
    assert len(data["optimizations"]) > 0

def test_rate_limiting(client, auth_headers):
    """Test rate limiting middleware"""
    # Make multiple requests in quick succession
    responses = []
    for _ in range(5):
        response = client.post(
            "/optimize/seo",
            headers=auth_headers,
            json={
                "content": "Test content",
                "content_type": "text"
            }
        )
        responses.append(response)
    
    # Check rate limit headers
    last_response = responses[-1]
    assert "X-RateLimit-Limit" in last_response.headers
    assert "X-RateLimit-Remaining" in last_response.headers
    assert "X-RateLimit-Reset" in last_response.headers

def test_authentication(client):
    """Test authentication requirements"""
    response = client.post(
        "/optimize/seo",
        json={
            "content": "Test content",
            "content_type": "text"
        }
    )
    assert response.status_code == 401  # Unauthorized

def test_subscription_restrictions(client, auth_headers, test_db):
    """Test subscription plan restrictions"""
    # Create free tier user
    db = TestingSessionLocal()
    user = User(
        email="free@example.com",
        username="freeuser",
        password_hash="hashed_password",
        subscription_plan="free"
    )
    db.add(user)
    db.commit()
    
    # Get token for free user
    free_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    free_headers = {"Authorization": f"Bearer {free_token}"}
    
    # Try to access pro features
    response = client.post(
        "/optimize/geo",
        headers=free_headers,
        json={
            "content": "Test content",
            "content_type": "text",
            "target_platforms": ["chatgpt"]
        }
    )
    assert response.status_code == 403  # Forbidden

def test_error_handling(client, auth_headers):
    """Test API error handling"""
    # Test invalid content
    response = client.post(
        "/optimize/seo",
        headers=auth_headers,
        json={
            "content": "",  # Empty content
            "content_type": "text"
        }
    )
    assert response.status_code == 400  # Bad request
    
    # Test invalid optimization goals
    response = client.post(
        "/optimize/geo",
        headers=auth_headers,
        json={
            "content": "Test content",
            "content_type": "text",
            "target_platforms": ["invalid_platform"]
        }
    )
    assert response.status_code == 400  # Bad request 