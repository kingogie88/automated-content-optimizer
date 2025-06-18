import pytest
from pathlib import Path
import json
from PIL import Image
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional

# Mock classes for testing
@dataclass
class MultiModalContent:
    text: str
    images: List[Dict[str, str]]
    audio_transcripts: List[Dict[str, str]]
    video_metadata: Dict
    structured_data: Dict

class MockProcessor:
    """Mock processor for testing core functionality."""
    
    async def process_content(
        self,
        text: Optional[str] = None,
        images: List[str] = None,
        audio_files: List[str] = None,
        video_files: List[str] = None,
        structured_data: Dict = None
    ) -> MultiModalContent:
        """Process content without external dependencies."""
        result = MultiModalContent(
            text="",
            images=[],
            audio_transcripts=[],
            video_metadata={},
            structured_data={}
        )
        
        if text:
            result.text = self._process_text(text)
        
        if images:
            for image_path in images:
                result.images.append(self._process_image(image_path))
        
        if structured_data:
            result.structured_data = self._process_structured_data(structured_data)
        
        return result
    
    def _process_text(self, text: str) -> str:
        """Basic text processing."""
        # Add mock formatting
        lines = text.split("\n")
        processed = []
        for line in lines:
            if line.startswith("#"):
                processed.append(f"HEADING: {line}")
            else:
                processed.append(f"CONTENT: {line}")
        return "\n".join(processed)
    
    def _process_image(self, image_path: str) -> Dict[str, str]:
        """Basic image processing."""
        try:
            img = Image.open(image_path)
            return {
                "path": image_path,
                "size": f"{img.size[0]}x{img.size[1]}",
                "format": img.format or "unknown"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _process_structured_data(self, data: Dict) -> Dict:
        """Basic structured data processing."""
        return {
            "processed": True,
            "fields": list(data.keys()),
            "original": data
        }

@pytest.fixture
def processor():
    return MockProcessor()

@pytest.fixture
def sample_text():
    return """# Sample Title
This is a test paragraph.

## Section 1
Some content here."""

@pytest.fixture
def sample_image(tmp_path):
    """Create a sample test image."""
    img_path = tmp_path / "test_image.png"
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    img.save(img_path)
    return str(img_path)

@pytest.fixture
def sample_structured_data():
    return {
        "title": "Test Document",
        "author": "Test Author",
        "tags": ["test", "sample"]
    }

class TestMultiModalProcessor:
    @pytest.mark.asyncio
    async def test_process_text(self, processor, sample_text):
        """Test text processing functionality."""
        result = await processor.process_content(text=sample_text)
        assert isinstance(result, MultiModalContent)
        assert result.text
        assert "HEADING: # Sample Title" in result.text
        assert "CONTENT: This is a test paragraph" in result.text

    @pytest.mark.asyncio
    async def test_process_image(self, processor, sample_image):
        """Test image processing functionality."""
        result = await processor.process_content(images=[sample_image])
        assert isinstance(result, MultiModalContent)
        assert len(result.images) == 1
        assert "size" in result.images[0]
        assert "format" in result.images[0]

    @pytest.mark.asyncio
    async def test_process_structured_data(self, processor, sample_structured_data):
        """Test structured data processing."""
        result = await processor.process_content(structured_data=sample_structured_data)
        assert isinstance(result, MultiModalContent)
        assert result.structured_data["processed"] is True
        assert "title" in result.structured_data["original"]

    @pytest.mark.asyncio
    async def test_process_multiple_content_types(
        self, processor, sample_text, sample_image, sample_structured_data
    ):
        """Test processing multiple content types together."""
        result = await processor.process_content(
            text=sample_text,
            images=[sample_image],
            structured_data=sample_structured_data
        )
        assert isinstance(result, MultiModalContent)
        assert result.text
        assert len(result.images) == 1
        assert result.structured_data["processed"] is True

    @pytest.mark.asyncio
    async def test_error_handling(self, processor):
        """Test error handling for invalid inputs."""
        result = await processor.process_content(
            images=["nonexistent.jpg"]
        )
        assert isinstance(result, MultiModalContent)
        assert "error" in result.images[0] 