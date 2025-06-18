import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import io
from src.core.content_processor import ContentProcessor

@pytest.fixture
def content_processor():
    return ContentProcessor()

@pytest.fixture
def sample_text():
    return """
    This is a sample text.
    It has multiple sentences.
    And multiple paragraphs.

    This is another paragraph.
    """

@pytest.fixture
def sample_html():
    return """
    <html>
        <body>
            <h1>Sample Title</h1>
            <p>This is a paragraph.</p>
            <p>This is another paragraph.</p>
        </body>
    </html>
    """

@pytest.fixture
def sample_pdf_bytes():
    return b'%PDF-1.4\n%...'

@pytest.fixture
def sample_docx_bytes():
    return b'PK\x03\x04...'

def test_content_processor_initialization(content_processor):
    """Test content processor initialization"""
    assert content_processor is not None
    assert hasattr(content_processor, 'supported_types')
    assert isinstance(content_processor.supported_types, dict)

def test_process_text(content_processor, sample_text):
    """Test text processing"""
    result = content_processor.process_content(sample_text)
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["word_count"] > 0
    assert result["metadata"]["sentence_count"] > 0
    assert result["metadata"]["paragraph_count"] > 0
    assert not result["metadata"]["is_html"]

def test_process_html(content_processor, sample_html):
    """Test HTML processing"""
    result = content_processor.process_content(sample_html)
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["is_html"]
    assert "Sample Title" in result["content"]

def test_detect_content_type(content_processor):
    """Test content type detection"""
    # Test text detection
    assert content_processor._detect_content_type("plain text") == "text"
    assert content_processor._detect_content_type("http://example.com") == "text"
    
    # Test file path detection
    with patch('os.path.isfile', return_value=True), \
         patch('magic.from_file', return_value='text/plain'):
        assert content_processor._detect_content_type("test.txt") == "text"
    
    # Test bytes detection
    with patch('magic.from_buffer', return_value='image/jpeg'):
        assert content_processor._detect_content_type(b'fake image data') == "image"

def test_mime_to_type(content_processor):
    """Test MIME type conversion"""
    assert content_processor._mime_to_type('text/plain') == 'text'
    assert content_processor._mime_to_type('image/jpeg') == 'image'
    assert content_processor._mime_to_type('application/pdf') == 'document'
    
    with pytest.raises(ValueError):
        content_processor._mime_to_type('application/unknown')

def test_process_document(content_processor):
    """Test document processing"""
    # Test PDF processing
    with patch('PyPDF2.PdfReader') as mock_pdf:
        mock_page = Mock()
        mock_page.extract_text.return_value = "PDF content"
        mock_pdf.return_value.pages = [mock_page]
        
        result = content_processor._process_document("test.pdf")
        assert isinstance(result, dict)
        assert "content" in result
        assert "metadata" in result
    
    # Test DOCX processing
    with patch('docx.Document') as mock_docx:
        mock_para = Mock()
        mock_para.text = "DOCX content"
        mock_docx.return_value.paragraphs = [mock_para]
        
        result = content_processor._process_document("test.docx")
        assert isinstance(result, dict)
        assert "content" in result
        assert "metadata" in result

def test_process_image(content_processor):
    """Test image processing"""
    # Create a mock image
    mock_image = Mock()
    mock_image.format = "JPEG"
    mock_image.mode = "RGB"
    mock_image.size = (800, 600)
    mock_image.width = 800
    mock_image.height = 600
    
    with patch('PIL.Image.open', return_value=mock_image), \
         patch('pytesseract.image_to_string', return_value="Extracted text"):
        
        result = content_processor._process_image("test.jpg")
        assert isinstance(result, dict)
        assert "content" in result
        assert "metadata" in result
        assert result["metadata"]["format"] == "JPEG"
        assert result["metadata"]["width"] == 800

def test_process_audio(content_processor):
    """Test audio processing"""
    result = content_processor._process_audio("test.mp3")
    assert isinstance(result, dict)
    assert result["metadata"]["type"] == "audio"
    assert result["metadata"]["status"] == "not_implemented"

def test_process_video(content_processor):
    """Test video processing"""
    result = content_processor._process_video("test.mp4")
    assert isinstance(result, dict)
    assert result["metadata"]["type"] == "video"
    assert result["metadata"]["status"] == "not_implemented"

def test_extract_metadata(content_processor, sample_text):
    """Test metadata extraction"""
    metadata = content_processor.extract_metadata(sample_text)
    assert isinstance(metadata, dict)
    assert "word_count" in metadata
    assert "sentence_count" in metadata
    assert "paragraph_count" in metadata

def test_get_content_type(content_processor):
    """Test content type retrieval"""
    assert content_processor.get_content_type("test.txt") == "text"
    assert content_processor.get_content_type("test.jpg") == "image"
    assert content_processor.get_content_type("test.pdf") == "document"

def test_is_supported_type(content_processor):
    """Test supported type checking"""
    assert content_processor.is_supported_type("text")
    assert content_processor.is_supported_type("image")
    assert not content_processor.is_supported_type("unknown")

def test_error_handling(content_processor):
    """Test error handling"""
    with pytest.raises(ValueError):
        content_processor.process_content("test.xyz")
    
    with pytest.raises(ValueError):
        content_processor._mime_to_type("application/unknown")
    
    with pytest.raises(ValueError):
        content_processor._process_document("test.xyz")

def test_edge_cases(content_processor):
    """Test edge cases"""
    # Test empty content
    result = content_processor.process_content("")
    assert result["metadata"]["word_count"] == 0
    
    # Test content with special characters
    special_text = "!@#$%^&*()_+{}|:<>?~`-=[]\\;',./"
    result = content_processor.process_content(special_text)
    assert result["metadata"]["word_count"] > 0
    
    # Test content with non-English characters
    non_english = "人工智能正在改变我们的生活和工作方式。"
    result = content_processor.process_content(non_english)
    assert result["metadata"]["word_count"] > 0

@pytest.mark.parametrize("content_type,expected_metadata", [
    ("text", ["word_count", "sentence_count", "paragraph_count"]),
    ("image", ["format", "mode", "size", "width", "height"]),
    ("document", ["word_count", "sentence_count", "paragraph_count"]),
    ("audio", ["type", "status"]),
    ("video", ["type", "status"])
])
def test_metadata_structure(content_processor, content_type, expected_metadata):
    """Test metadata structure for different content types"""
    # Create mock content based on type
    if content_type == "text":
        content = "Sample text content"
    elif content_type == "image":
        content = "test.jpg"
    elif content_type == "document":
        content = "test.pdf"
    else:
        content = f"test.{content_type}"
    
    # Process content and check metadata
    with patch('os.path.isfile', return_value=True), \
         patch('magic.from_file', return_value=f'{content_type}/test'):
        result = content_processor.process_content(content)
        assert all(key in result["metadata"] for key in expected_metadata) 