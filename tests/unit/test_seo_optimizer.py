import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.seo_optimizer import SEOOptimizer

@pytest.fixture
def seo_optimizer():
    with patch('src.core.seo_optimizer.nltk.download') as mock_download, \
         patch('src.core.seo_optimizer.nltk.data.find') as mock_find, \
         patch('src.core.seo_optimizer.BeautifulSoup') as mock_soup:
        
        mock_find.return_value = True
        mock_soup.return_value = Mock()
        return SEOOptimizer()

@pytest.fixture
def sample_content():
    return """
    <h1>Artificial Intelligence in Modern Business</h1>
    
    <h2>Introduction to AI</h2>
    <p>Artificial Intelligence (AI) is revolutionizing how businesses operate. 
    Companies are increasingly adopting AI solutions to improve efficiency and gain competitive advantages.</p>
    
    <h2>Key Applications</h2>
    <p>Machine learning algorithms help businesses analyze customer data and make better decisions. 
    Natural Language Processing enables automated customer service through chatbots.</p>
    
    <h2>Future Outlook</h2>
    <p>The future of AI in business looks promising, with new applications emerging every day. 
    Companies that embrace AI early will have a significant advantage in their respective markets.</p>
    """

@pytest.fixture
def target_keywords():
    return ["artificial intelligence", "machine learning", "business", "AI solutions"]

def test_seo_optimizer_initialization(seo_optimizer):
    """Test SEO optimizer initialization"""
    assert seo_optimizer is not None
    assert hasattr(seo_optimizer, 'stop_words')
    assert isinstance(seo_optimizer.stop_words, set)

def test_optimize_content_basic(seo_optimizer, sample_content, target_keywords):
    """Test basic content optimization"""
    result = seo_optimizer.optimize_content(
        content=sample_content,
        target_keywords=target_keywords,
        min_word_count=300,
        max_keyword_density=0.03
    )
    
    assert isinstance(result, dict)
    assert "original_content" in result
    assert "optimized_content" in result
    assert "metrics" in result
    assert "suggestions" in result
    assert "score" in result
    assert "meta_tags" in result
    assert isinstance(result["score"], int)

def test_analyze_keywords(seo_optimizer, sample_content, target_keywords):
    """Test keyword analysis"""
    metrics = seo_optimizer._analyze_keywords(
        content=sample_content,
        target_keywords=target_keywords,
        max_density=0.03
    )
    
    assert isinstance(metrics, dict)
    assert "keyword_density" in metrics
    assert "keyword_count" in metrics
    assert "keyword_positions" in metrics
    
    for keyword in target_keywords:
        assert keyword in metrics["keyword_density"]
        assert keyword in metrics["keyword_count"]
        assert keyword in metrics["keyword_positions"]

def test_analyze_readability(seo_optimizer, sample_content):
    """Test readability analysis"""
    metrics = seo_optimizer._analyze_readability(sample_content)
    
    assert isinstance(metrics, dict)
    assert "avg_sentence_length" in metrics
    assert "avg_word_length" in metrics
    assert "sentence_count" in metrics
    assert "paragraph_count" in metrics
    
    assert metrics["sentence_count"] > 0
    assert metrics["paragraph_count"] > 0

def test_generate_meta_suggestions(seo_optimizer, sample_content, target_keywords):
    """Test meta tag suggestions generation"""
    meta_tags = seo_optimizer._generate_meta_suggestions(
        content=sample_content,
        target_keywords=target_keywords
    )
    
    assert isinstance(meta_tags, dict)
    assert "title" in meta_tags
    assert "description" in meta_tags
    assert "keywords" in meta_tags
    
    assert len(meta_tags["title"]) > 0
    assert len(meta_tags["description"]) <= 160
    assert len(meta_tags["keywords"]) > 0

def test_analyze_structure(seo_optimizer, sample_content):
    """Test content structure analysis"""
    structure = seo_optimizer._analyze_structure(sample_content)
    
    assert isinstance(structure, dict)
    assert "headings" in structure
    assert "links" in structure
    assert "images" in structure
    assert "lists" in structure
    
    assert structure["headings"]["h1"] > 0
    assert structure["headings"]["h2"] > 0

def test_calculate_score(seo_optimizer):
    """Test score calculation"""
    metrics = {
        "word_count": 250,
        "avg_sentence_length": 30,
        "headings": {"h1": 0, "h2": 2},
        "links": 0,
        "issues": ["Keyword density too high"]
    }
    
    score = seo_optimizer._calculate_score(metrics)
    assert isinstance(score, int)
    assert 0 <= score <= 100

def test_generate_suggestions(seo_optimizer):
    """Test suggestion generation"""
    metrics = {
        "word_count": 250,
        "avg_sentence_length": 30,
        "headings": {"h1": 0, "h2": 2},
        "links": 0,
        "images": 0
    }
    
    suggestions = seo_optimizer._generate_suggestions(metrics)
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    assert all(isinstance(s, str) for s in suggestions)

def test_optimize_content_structure(seo_optimizer, sample_content):
    """Test content structure optimization"""
    suggestions = [
        "Add an H1 heading to your content",
        "Consider adding H2 subheadings to structure your content",
        "Add relevant internal or external links"
    ]
    
    optimized_content = seo_optimizer._optimize_content_structure(
        sample_content,
        suggestions
    )
    
    assert isinstance(optimized_content, str)
    assert len(optimized_content) > 0

def test_error_handling(seo_optimizer):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        seo_optimizer.optimize_content(content="")
    
    with pytest.raises(ValueError):
        seo_optimizer.optimize_content(
            content="Valid content",
            max_keyword_density=-0.1
        )

def test_edge_cases(seo_optimizer):
    """Test edge cases"""
    # Test with very long content
    long_content = "<h1>Title</h1><p>" + "word " * 10000 + "</p>"
    result = seo_optimizer.optimize_content(
        content=long_content,
        target_keywords=["test"],
        min_word_count=100,
        max_keyword_density=0.03
    )
    assert isinstance(result, dict)
    assert "score" in result
    
    # Test with special characters
    special_content = "<h1>!@#$%^&*()_+{}|:<>?~`-=[]\\;',./</h1>"
    result = seo_optimizer.optimize_content(
        content=special_content,
        target_keywords=["test"],
        min_word_count=100,
        max_keyword_density=0.03
    )
    assert isinstance(result, dict)
    assert "score" in result
    
    # Test with non-English content
    non_english = "<h1>人工智能</h1><p>人工智能正在改变我们的生活和工作方式。</p>"
    result = seo_optimizer.optimize_content(
        content=non_english,
        target_keywords=["人工智能"],
        min_word_count=100,
        max_keyword_density=0.03
    )
    assert isinstance(result, dict)
    assert "score" in result

@pytest.mark.parametrize("content_type,expected_structure", [
    ("html", {"headings": {"h1": 1, "h2": 2}, "links": 0, "images": 0, "lists": 0}),
    ("plain", {"headings": {}, "links": 0, "images": 0, "lists": 0}),
    ("mixed", {"headings": {"h1": 1}, "links": 1, "images": 1, "lists": 1})
])
def test_content_structure_analysis(seo_optimizer, content_type, expected_structure):
    """Test content structure analysis for different content types"""
    if content_type == "html":
        content = "<h1>Title</h1><h2>Subtitle 1</h2><h2>Subtitle 2</h2>"
    elif content_type == "plain":
        content = "This is plain text content without any HTML."
    else:  # mixed
        content = "<h1>Title</h1><a href='#'>Link</a><img src='test.jpg'><ul><li>Item</li></ul>"
    
    structure = seo_optimizer._analyze_structure(content)
    assert isinstance(structure, dict)
    
    for key, value in expected_structure.items():
        assert key in structure
        if key == "headings":
            assert all(k in structure[key] for k in value.keys())
            assert all(structure[key][k] == v for k, v in value.items())
        else:
            assert structure[key] == value 