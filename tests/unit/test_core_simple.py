"""Simple tests for core functionality with mocked dependencies."""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Optional

# Mock the heavy dependencies
with patch('transformers.pipeline') as mock_pipeline:
    mock_pipeline.return_value = Mock()
    
    with patch('spacy.load') as mock_spacy_load:
        mock_spacy_load.return_value = Mock()
        
        with patch('sentence_transformers.SentenceTransformer') as mock_transformer:
            mock_transformer.return_value = Mock()
            
            # Now we can import our core modules
            from src.core.seo_optimizer import SEOOptimizer
            from src.core.geo_optimizer import GEOOptimizer
            from src.core.content_processor import ContentProcessor

@pytest.fixture
def seo_optimizer():
    """Create a SEO optimizer instance with mocked dependencies."""
    with patch('nltk.corpus.stopwords.words') as mock_stopwords:
        mock_stopwords.return_value = ['the', 'a', 'an', 'and', 'or', 'but']
        return SEOOptimizer()

@pytest.fixture
def geo_optimizer():
    """Create a GEO optimizer instance with mocked dependencies."""
    with patch('spacy.load') as mock_spacy_load:
        mock_spacy_load.return_value = Mock()
        with patch('sentence_transformers.SentenceTransformer') as mock_transformer:
            mock_transformer.return_value = Mock()
            with patch('transformers.pipeline') as mock_pipeline:
                mock_pipeline.return_value = Mock()
                return GEOOptimizer()

@pytest.fixture
def content_processor():
    """Create a content processor instance with mocked dependencies."""
    with patch('transformers.pipeline') as mock_pipeline:
        mock_pipeline.return_value = Mock()
        with patch('whisper.load_model') as mock_whisper:
            mock_whisper.return_value = Mock()
            return ContentProcessor()

def test_seo_optimizer_initialization(seo_optimizer):
    """Test SEO optimizer initialization."""
    assert seo_optimizer is not None
    assert hasattr(seo_optimizer, 'stop_words')

def test_seo_optimizer_optimize_content(seo_optimizer):
    """Test SEO optimizer content optimization."""
    content = "This is a test article about SEO optimization."
    result = seo_optimizer.optimize_content(
        content=content,
        target_keywords=["seo", "optimization"]
    )
    
    assert isinstance(result, dict)
    assert "original_content" in result
    assert "optimized_content" in result
    assert "metrics" in result
    assert "suggestions" in result
    assert "score" in result

def test_geo_optimizer_initialization(geo_optimizer):
    """Test GEO optimizer initialization."""
    assert geo_optimizer is not None
    assert hasattr(geo_optimizer, 'nlp')

def test_geo_optimizer_optimize_content(geo_optimizer):
    """Test GEO optimizer content optimization."""
    content = "This is a test article for AI platforms."
    result = geo_optimizer.optimize_content(
        content=content,
        target_platforms=["chatgpt", "claude"]
    )
    
    assert isinstance(result, dict)
    assert "original_content" in result
    assert "optimized_content" in result
    assert "metrics" in result
    assert "suggestions" in result
    assert "score" in result

def test_content_processor_initialization(content_processor):
    """Test content processor initialization."""
    assert content_processor is not None
    assert hasattr(content_processor, 'supported_types')

def test_content_processor_process_text(content_processor):
    """Test content processor text processing."""
    content = "This is a test text content."
    result = content_processor.process_content(content)
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert "content_type" in result

def test_content_processor_process_file(content_processor):
    """Test content processor file processing."""
    # Create a temporary text file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is test content from a file.")
        temp_file = f.name
    
    try:
        result = content_processor.process_content(temp_file)
        assert isinstance(result, dict)
        assert "content" in result
        assert "metadata" in result
        assert "content_type" in result
    finally:
        os.unlink(temp_file) 