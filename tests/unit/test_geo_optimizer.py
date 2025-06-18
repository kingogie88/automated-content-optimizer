import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.geo_optimizer import GEOOptimizer

@pytest.fixture
def geo_optimizer():
    with patch('src.core.geo_optimizer.spacy.load') as mock_spacy, \
         patch('src.core.geo_optimizer.SentenceTransformer') as mock_transformer, \
         patch('src.core.geo_optimizer.pipeline') as mock_pipeline:
        
        mock_nlp = Mock()
        mock_nlp.return_value = Mock()
        mock_spacy.return_value = mock_nlp
        
        mock_transformer.return_value = Mock()
        mock_pipeline.return_value = Mock()
        
        return GEOOptimizer()

@pytest.fixture
def sample_content():
    return """
    Artificial Intelligence (AI) is transforming the way we live and work. 
    Machine learning algorithms can now process vast amounts of data to make predictions.
    Deep learning models have achieved remarkable success in image recognition tasks.
    Natural Language Processing (NLP) enables computers to understand human language.
    """

@pytest.fixture
def target_platforms():
    return ["chatgpt", "claude", "voice"]

@pytest.fixture
def optimization_goals():
    return ["context", "factual", "voice_search"]

def test_geo_optimizer_initialization(geo_optimizer):
    """Test GEO optimizer initialization"""
    assert geo_optimizer is not None
    assert hasattr(geo_optimizer, 'nlp')
    assert hasattr(geo_optimizer, 'transformer')
    assert hasattr(geo_optimizer, 'classifier')

def test_optimize_content_basic(geo_optimizer, sample_content, target_platforms, optimization_goals):
    """Test basic content optimization"""
    result = geo_optimizer.optimize_content(
        content=sample_content,
        target_platforms=target_platforms,
        optimization_goals=optimization_goals
    )
    
    assert isinstance(result, dict)
    assert "original_content" in result
    assert "optimized_content" in result
    assert "metrics" in result
    assert "suggestions" in result
    assert "score" in result
    assert isinstance(result["score"], (int, float))

def test_analyze_context_clarity(geo_optimizer, sample_content):
    """Test context clarity analysis"""
    metrics = geo_optimizer._analyze_context_clarity(sample_content)
    
    assert isinstance(metrics, dict)
    assert "sentence_count" in metrics
    assert "avg_sentence_length" in metrics
    assert "unique_entities" in metrics
    assert "complex_sentence_ratio" in metrics
    assert "transition_density" in metrics

def test_optimize_for_voice_search(geo_optimizer, sample_content):
    """Test voice search optimization"""
    metrics = geo_optimizer._optimize_for_voice_search(sample_content)
    
    assert isinstance(metrics, dict)
    assert "question_count" in metrics
    assert "conversational_phrases" in metrics
    assert "natural_language_score" in metrics

def test_optimize_for_platform(geo_optimizer, sample_content):
    """Test platform-specific optimization"""
    platforms = ["chatgpt", "claude", "voice"]
    
    for platform in platforms:
        metrics = geo_optimizer._optimize_for_platform(sample_content, platform)
        assert isinstance(metrics, dict)
        assert "platform_score" in metrics
        assert "suggestions" in metrics

def test_calculate_score(geo_optimizer):
    """Test score calculation"""
    metrics = {
        "context_clarity": {
            "complex_sentence_ratio": 0.4,
            "transition_density": 0.1
        },
        "factual_consistency": {
            "citation_count": 0,
            "verifiable_statements": 2
        },
        "voice_search": {
            "natural_language_score": 60,
            "conversational_phrases": 0
        }
    }
    
    score = geo_optimizer._calculate_score(metrics)
    assert isinstance(score, int)
    assert 0 <= score <= 100

def test_generate_suggestions(geo_optimizer):
    """Test suggestion generation"""
    metrics = {
        "context_clarity": {
            "complex_sentence_ratio": 0.4,
            "transition_density": 0.1
        },
        "factual_consistency": {
            "citation_count": 0,
            "verifiable_statements": 2
        },
        "voice_search": {
            "question_count": 0,
            "conversational_phrases": 0
        }
    }
    
    suggestions = geo_optimizer._generate_suggestions(metrics)
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    assert all(isinstance(s, str) for s in suggestions)

def test_apply_optimizations(geo_optimizer, sample_content, target_platforms):
    """Test optimization application"""
    suggestions = [
        "Simplify complex sentences for better AI comprehension",
        "Add more transition words to improve flow",
        "Add citations or references to support claims"
    ]
    
    optimized_content = geo_optimizer._apply_optimizations(
        sample_content,
        suggestions,
        target_platforms
    )
    
    assert isinstance(optimized_content, str)
    assert len(optimized_content) > 0

def test_error_handling(geo_optimizer):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        geo_optimizer.optimize_content(content="")
    
    with pytest.raises(ValueError):
        geo_optimizer.optimize_content(
            content="Valid content",
            target_platforms=[]
        )
    
    with pytest.raises(ValueError):
        geo_optimizer.optimize_content(
            content="Valid content",
            optimization_goals=[]
        )

def test_edge_cases(geo_optimizer):
    """Test edge cases"""
    # Test with very long content
    long_content = "word " * 10000
    result = geo_optimizer.optimize_content(
        content=long_content,
        target_platforms=["chatgpt"],
        optimization_goals=["context"]
    )
    assert isinstance(result, dict)
    assert "score" in result
    
    # Test with special characters
    special_content = "!@#$%^&*()_+{}|:<>?~`-=[]\\;',./"
    result = geo_optimizer.optimize_content(
        content=special_content,
        target_platforms=["chatgpt"],
        optimization_goals=["context"]
    )
    assert isinstance(result, dict)
    assert "score" in result
    
    # Test with non-English content
    non_english = "人工智能正在改变我们的生活和工作方式。"
    result = geo_optimizer.optimize_content(
        content=non_english,
        target_platforms=["chatgpt"],
        optimization_goals=["context"]
    )
    assert isinstance(result, dict)
    assert "score" in result

@pytest.mark.parametrize("platform,expected_metrics", [
    ("chatgpt", ["structure_score", "clarity_score", "context_score"]),
    ("claude", ["platform_score"]),
    ("voice", ["question_count", "conversational_phrases", "natural_language_score"])
])
def test_platform_metrics(geo_optimizer, sample_content, platform, expected_metrics):
    """Test platform-specific metrics"""
    metrics = geo_optimizer._optimize_for_platform(sample_content, platform)
    
    if platform == "chatgpt":
        assert all(metric in metrics["chatgpt_metrics"] for metric in expected_metrics)
    elif platform == "claude":
        assert all(metric in metrics for metric in expected_metrics)
    elif platform == "voice":
        assert all(metric in metrics["voice_search"] for metric in expected_metrics) 