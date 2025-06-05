import pytest
from core.geo.optimizer import GEOOptimizer
from unittest.mock import Mock, patch

@pytest.fixture
def geo_optimizer():
    return GEOOptimizer()

@pytest.fixture
def sample_content():
    return """
    How to Train a Machine Learning Model

    Let me explain the process of training a machine learning model. 
    First, you need to gather and prepare your data. This includes cleaning the data 
    and splitting it into training and testing sets.

    Here are the key steps:
    1. Data collection and preprocessing
    2. Feature selection and engineering
    3. Model selection
    4. Training and validation
    5. Testing and evaluation

    Remember, the quality of your data significantly impacts the model's performance.
    """

def test_optimize_content_basic(geo_optimizer, sample_content):
    """Test basic content optimization for AI platforms"""
    result = geo_optimizer.optimize_content(
        content=sample_content,
        target_platforms=["chatgpt", "claude"],
        optimization_goals=["context", "factual"]
    )
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "suggestions" in result
    assert "metrics" in result
    assert "optimized_content" in result
    assert result["score"] >= 0 and result["score"] <= 100

def test_context_clarity_analysis(geo_optimizer, sample_content):
    """Test context clarity metrics"""
    result = geo_optimizer.optimize_content(content=sample_content)
    metrics = result["metrics"]
    
    assert "context_clarity" in metrics
    clarity = metrics["context_clarity"]
    assert "sentence_count" in clarity
    assert "avg_sentence_length" in clarity
    assert "complex_sentence_ratio" in clarity
    assert "transition_density" in clarity
    
    assert clarity["sentence_count"] > 0
    assert 0 <= clarity["complex_sentence_ratio"] <= 1

def test_factual_consistency(geo_optimizer, sample_content):
    """Test factual consistency analysis"""
    result = geo_optimizer.optimize_content(
        content=sample_content,
        optimization_goals=["factual"]
    )
    
    metrics = result["metrics"]
    assert "factual_consistency" in metrics
    factual = metrics["factual_consistency"]
    
    assert "claim_count" in factual
    assert "citation_count" in factual
    assert "verifiable_statements" in factual
    assert factual["verifiable_statements"] >= 0

def test_voice_search_optimization(geo_optimizer):
    """Test voice search optimization"""
    voice_content = """
    What is machine learning?
    Machine learning is a type of artificial intelligence that allows computers to learn
    from data without being explicitly programmed. Let me explain how it works.
    
    Think about how you would teach a child to recognize cats. Similarly, machine
    learning models learn from examples.
    """
    
    result = geo_optimizer.optimize_content(
        content=voice_content,
        optimization_goals=["voice_search"]
    )
    
    metrics = result["metrics"]
    assert "voice_search" in metrics
    voice = metrics["voice_search"]
    
    assert "question_count" in voice
    assert "conversational_phrases" in voice
    assert "natural_language_score" in voice
    assert voice["question_count"] > 0

@pytest.mark.parametrize("platform", ["chatgpt", "claude", "voice"])
def test_platform_specific_optimization(geo_optimizer, sample_content, platform):
    """Test optimization for specific AI platforms"""
    result = geo_optimizer.optimize_content(
        content=sample_content,
        target_platforms=[platform]
    )
    
    metrics = result["metrics"]
    assert f"{platform}_metrics" in metrics
    platform_metrics = metrics[f"{platform}_metrics"]
    
    if platform in ["chatgpt", "claude"]:
        assert "structure_score" in platform_metrics
        assert "clarity_score" in platform_metrics
        assert "context_score" in platform_metrics
    elif platform == "voice":
        assert "natural_language_score" in platform_metrics

def test_combined_optimization(geo_optimizer, sample_content):
    """Test combined optimization for multiple platforms"""
    result = geo_optimizer.optimize_content(
        content=sample_content,
        target_platforms=["chatgpt", "claude", "voice"],
        optimization_goals=["context", "factual", "voice_search"]
    )
    
    assert all(
        f"{platform}_metrics" in result["metrics"]
        for platform in ["chatgpt", "claude"]
    )
    assert "voice_search" in result["metrics"]
    assert len(result["suggestions"]) > 0

def test_error_handling(geo_optimizer):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        geo_optimizer.optimize_content(content="")
    
    with pytest.raises(ValueError):
        geo_optimizer.optimize_content(
            content="Valid content",
            target_platforms=["invalid_platform"]
        )

@pytest.mark.asyncio
async def test_api_integration():
    """Test integration with AI APIs"""
    with patch("openai.ChatCompletion.create") as mock_openai:
        with patch("anthropic.Anthropic.messages.create") as mock_anthropic:
            # Mock API responses
            mock_openai.return_value = {"choices": [{"message": {"content": "Optimized content"}}]}
            mock_anthropic.return_value = Mock(content="Optimized content")
            
            optimizer = GEOOptimizer()
            result = optimizer.optimize_content(
                content="Test content",
                target_platforms=["chatgpt", "claude"]
            )
            
            assert mock_openai.called
            assert mock_anthropic.called
            assert "optimized_content" in result 