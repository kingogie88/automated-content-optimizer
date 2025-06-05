import pytest
from core.seo.optimizer import SEOOptimizer
from unittest.mock import Mock, patch

@pytest.fixture
def seo_optimizer():
    return SEOOptimizer()

@pytest.fixture
def sample_content():
    return """
    Machine Learning in Healthcare
    
    Artificial intelligence and machine learning are revolutionizing healthcare. 
    These technologies help doctors make better diagnoses and predict patient outcomes.
    Machine learning algorithms can analyze medical images with high accuracy.
    
    Key benefits include:
    - Early disease detection
    - Personalized treatment plans
    - Reduced medical errors
    - Improved patient care
    """

def test_optimize_content_basic(seo_optimizer, sample_content):
    """Test basic content optimization"""
    result = seo_optimizer.optimize_content(
        content=sample_content,
        target_keywords=["machine learning", "healthcare", "AI"]
    )
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "suggestions" in result
    assert "metrics" in result
    assert "optimized_content" in result
    assert result["score"] >= 0 and result["score"] <= 100

def test_keyword_analysis(seo_optimizer, sample_content):
    """Test keyword analysis functionality"""
    result = seo_optimizer.optimize_content(
        content=sample_content,
        target_keywords=["machine learning", "healthcare"]
    )
    
    metrics = result["metrics"]
    assert "keyword_metrics" in metrics
    assert "keyword_density" in metrics["keyword_metrics"]
    assert "keyword_count" in metrics["keyword_metrics"]
    
    # Check keyword density
    densities = metrics["keyword_metrics"]["keyword_density"]
    assert all(0 <= d <= 1 for d in densities.values())

def test_readability_analysis(seo_optimizer, sample_content):
    """Test readability metrics calculation"""
    result = seo_optimizer.optimize_content(content=sample_content)
    metrics = result["metrics"]
    
    assert "readability_metrics" in metrics
    readability = metrics["readability_metrics"]
    assert "avg_sentence_length" in readability
    assert "avg_word_length" in readability
    assert readability["avg_sentence_length"] > 0

def test_meta_suggestions(seo_optimizer, sample_content):
    """Test meta tag generation"""
    result = seo_optimizer.optimize_content(
        content=sample_content,
        target_keywords=["machine learning", "healthcare"]
    )
    
    assert "meta_tags" in result
    meta_tags = result["meta_tags"]
    assert "title" in meta_tags
    assert "description" in meta_tags
    assert len(meta_tags["description"]) <= 160  # SEO best practice

def test_content_structure(seo_optimizer):
    """Test HTML content structure analysis"""
    html_content = """
    <h1>Main Title</h1>
    <p>First paragraph with <a href="#">link</a>.</p>
    <h2>Subtitle</h2>
    <ul>
        <li>List item 1</li>
        <li>List item 2</li>
    </ul>
    <img src="image.jpg" alt="Test image">
    """
    
    result = seo_optimizer.optimize_content(content=html_content)
    structure = result["metrics"].get("structure_metrics", {})
    
    assert structure.get("headings", {}).get("h1") == 1
    assert structure.get("headings", {}).get("h2") == 1
    assert structure.get("links") == 1
    assert structure.get("images") == 1
    assert structure.get("lists") == 1

@pytest.mark.parametrize("word_count,expected_score", [
    (100, 80),  # Short content should get penalty
    (300, 90),  # Minimum recommended length
    (1000, 100)  # Optimal length
])
def test_content_length_scoring(seo_optimizer, word_count, expected_score):
    """Test content length impact on scoring"""
    content = " ".join(["word"] * word_count)
    result = seo_optimizer.optimize_content(content=content)
    assert abs(result["score"] - expected_score) <= 20

def test_error_handling(seo_optimizer):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        seo_optimizer.optimize_content(content="")
    
    with pytest.raises(ValueError):
        seo_optimizer.optimize_content(
            content="Valid content",
            max_keyword_density=-0.1
        ) 