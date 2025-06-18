"""
Simplified content processor for CI environments.
This version avoids heavy dependencies like pytesseract, numpy, etc.
"""

import os
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Union
import re
from bs4 import BeautifulSoup

class SimpleContentProcessor:
    """Simplified content processor for basic text and document processing."""
    
    def __init__(self):
        """Initialize the content processor."""
        self.supported_types = {
            "text": [".txt", ".md", ".html", ".htm"],
            "document": [".pdf", ".docx", ".doc"],
            "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "audio": [".mp3", ".wav", ".flac", ".m4a"],
            "video": [".mp4", ".avi", ".mov", ".mkv"]
        }
    
    def process_content(self, content: Union[str, bytes, Path], content_type: Optional[str] = None) -> Dict:
        """
        Process content and return analysis results.
        
        Args:
            content: Content to process (string, bytes, or file path)
            content_type: Optional content type hint
            
        Returns:
            Dictionary containing processed content and metadata
        """
        try:
            # Determine content type
            if content_type is None:
                content_type = self._detect_content_type(content)
            
            # Process based on type
            if content_type == "text":
                return self._process_text(content)
            elif content_type == "document":
                return self._process_document(content)
            elif content_type == "image":
                return self._process_image_simple(content)
            elif content_type == "audio":
                return self._process_audio_simple(content)
            elif content_type == "video":
                return self._process_video_simple(content)
            else:
                return self._process_unknown(content)
                
        except Exception as e:
            return {
                "content": str(content) if isinstance(content, (str, bytes)) else str(content),
                "metadata": {"error": str(e)},
                "content_type": "unknown"
            }
    
    def _detect_content_type(self, content: Union[str, bytes, Path]) -> str:
        """Detect content type based on file extension or content."""
        if isinstance(content, (str, Path)):
            if os.path.isfile(str(content)):
                ext = Path(content).suffix.lower()
                for content_type, extensions in self.supported_types.items():
                    if ext in extensions:
                        return content_type
            elif isinstance(content, str):
                # Check if it looks like HTML
                if content.strip().startswith('<'):
                    return "text"
                return "text"
        
        return "unknown"
    
    def _process_text(self, content: Union[str, bytes]) -> Dict:
        """Process text content."""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        
        # Basic text analysis
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Check for HTML
        is_html = content.strip().startswith('<')
        if is_html:
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            words = text_content.split()
            sentences = re.split(r'[.!?]+', text_content)
        
        return {
            "content": content,
            "metadata": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "is_html": is_html,
                "content_length": len(content)
            },
            "content_type": "text"
        }
    
    def _process_document(self, content: Union[str, bytes, Path]) -> Dict:
        """Process document content (simplified)."""
        if isinstance(content, (str, Path)) and os.path.isfile(str(content)):
            try:
                with open(content, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                return self._process_text(text_content)
            except Exception as e:
                return {
                    "content": f"Error reading document: {e}",
                    "metadata": {"error": str(e)},
                    "content_type": "document"
                }
        else:
            return self._process_text(content)
    
    def _process_image_simple(self, content: Union[str, bytes, Path]) -> Dict:
        """Process image content (simplified - no OCR)."""
        if isinstance(content, (str, Path)) and os.path.isfile(str(content)):
            file_size = os.path.getsize(content)
            return {
                "content": f"Image file: {Path(content).name}",
                "metadata": {
                    "file_size": file_size,
                    "file_type": "image",
                    "ocr_available": False,
                    "note": "OCR not available in simplified mode"
                },
                "content_type": "image"
            }
        else:
            return {
                "content": "Image data (binary)",
                "metadata": {"note": "Image processing not available in simplified mode"},
                "content_type": "image"
            }
    
    def _process_audio_simple(self, content: Union[str, bytes, Path]) -> Dict:
        """Process audio content (simplified)."""
        if isinstance(content, (str, Path)) and os.path.isfile(str(content)):
            file_size = os.path.getsize(content)
            return {
                "content": f"Audio file: {Path(content).name}",
                "metadata": {
                    "file_size": file_size,
                    "file_type": "audio",
                    "transcription_available": False,
                    "note": "Audio transcription not available in simplified mode"
                },
                "content_type": "audio"
            }
        else:
            return {
                "content": "Audio data (binary)",
                "metadata": {"note": "Audio processing not available in simplified mode"},
                "content_type": "audio"
            }
    
    def _process_video_simple(self, content: Union[str, bytes, Path]) -> Dict:
        """Process video content (simplified)."""
        if isinstance(content, (str, Path)) and os.path.isfile(str(content)):
            file_size = os.path.getsize(content)
            return {
                "content": f"Video file: {Path(content).name}",
                "metadata": {
                    "file_size": file_size,
                    "file_type": "video",
                    "analysis_available": False,
                    "note": "Video analysis not available in simplified mode"
                },
                "content_type": "video"
            }
        else:
            return {
                "content": "Video data (binary)",
                "metadata": {"note": "Video processing not available in simplified mode"},
                "content_type": "video"
            }
    
    def _process_unknown(self, content: Union[str, bytes, Path]) -> Dict:
        """Process unknown content type."""
        return {
            "content": str(content) if isinstance(content, (str, bytes)) else str(content),
            "metadata": {"note": "Unknown content type"},
            "content_type": "unknown"
        }
    
    def is_supported(self, content_type: str) -> bool:
        """Check if content type is supported."""
        return content_type in self.supported_types 