from typing import Dict, List, Union, Optional
from dataclasses import dataclass
import json
from PIL import Image
import pytesseract
import whisper
from transformers import pipeline
import os
import mimetypes
from pathlib import Path
import magic
import docx
from PyPDF2 import PdfReader
import numpy as np
from bs4 import BeautifulSoup
import re
import io

@dataclass
class MultiModalContent:
    text: str
    images: List[Dict[str, str]]  # Image descriptions and metadata
    audio_transcripts: List[Dict[str, str]]
    video_metadata: Dict[str, any]
    structured_data: Dict[str, any]

class MultiModalProcessor:
    """
    Process and optimize multiple content types for AI understanding.
    """
    
    def __init__(self):
        self.image_captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
        self.audio_model = whisper.load_model("base")
        self.text_classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
        
    async def process_content(
        self,
        text: Optional[str] = None,
        images: List[str] = None,
        audio_files: List[str] = None,
        video_files: List[str] = None,
        structured_data: Dict = None
    ) -> MultiModalContent:
        """Process multiple content types into an optimized format."""
        
        processed_content = MultiModalContent(
            text="",
            images=[],
            audio_transcripts=[],
            video_metadata={},
            structured_data={}
        )
        
        # Process text content
        if text:
            processed_content.text = await self._process_text(text)
        
        # Process images
        if images:
            for image_path in images:
                image_data = await self._process_image(image_path)
                processed_content.images.append(image_data)
        
        # Process audio
        if audio_files:
            for audio_path in audio_files:
                transcript = await self._process_audio(audio_path)
                processed_content.audio_transcripts.append(transcript)
        
        # Process video
        if video_files:
            for video_path in video_files:
                metadata = await self._process_video(video_path)
                processed_content.video_metadata.update(metadata)
        
        # Process structured data
        if structured_data:
            processed_content.structured_data = self._process_structured_data(structured_data)
        
        return processed_content
    
    async def _process_text(self, text: str) -> str:
        """Enhance text content with semantic markers and structure."""
        # Classify content type
        content_type = self.text_classifier(text, candidate_labels=[
            "article", "tutorial", "documentation", "conversation"
        ])
        
        # Apply type-specific optimization
        if content_type[0]["label"] == "article":
            return self._optimize_article(text)
        elif content_type[0]["label"] == "tutorial":
            return self._optimize_tutorial(text)
        elif content_type[0]["label"] == "documentation":
            return self._optimize_documentation(text)
        else:
            return self._optimize_general(text)
    
    async def _process_image(self, image_path: str) -> Dict[str, str]:
        """Extract and optimize image content."""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Extract text from image
            ocr_text = pytesseract.image_to_string(image)
            
            # Generate image description
            caption = self.image_captioner(image)[0]["generated_text"]
            
            return {
                "caption": caption,
                "ocr_text": ocr_text,
                "alt_text": self._generate_alt_text(caption, ocr_text),
                "metadata": self._extract_image_metadata(image)
            }
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            return {"error": str(e)}
    
    async def _process_audio(self, audio_path: str) -> Dict[str, str]:
        """Transcribe and optimize audio content."""
        try:
            # Transcribe audio
            result = self.audio_model.transcribe(audio_path)
            
            return {
                "transcript": result["text"],
                "segments": result["segments"],
                "language": result["language"],
                "metadata": self._extract_audio_metadata(audio_path)
            }
        except Exception as e:
            print(f"Error processing audio {audio_path}: {str(e)}")
            return {"error": str(e)}
    
    async def _process_video(self, video_path: str) -> Dict[str, any]:
        """Extract and optimize video content."""
        try:
            # Extract video frames
            frames = self._extract_key_frames(video_path)
            
            # Process each frame
            frame_data = []
            for frame in frames:
                frame_info = await self._process_image(frame)
                frame_data.append(frame_info)
            
            # Extract audio
            audio_track = self._extract_audio_track(video_path)
            audio_data = await self._process_audio(audio_track)
            
            return {
                "frames": frame_data,
                "audio": audio_data,
                "metadata": self._extract_video_metadata(video_path)
            }
        except Exception as e:
            print(f"Error processing video {video_path}: {str(e)}")
            return {"error": str(e)}
    
    def _process_structured_data(self, data: Dict) -> Dict:
        """Optimize structured data for AI understanding."""
        try:
            # Convert to standard format
            normalized_data = self._normalize_structured_data(data)
            
            # Add semantic context
            enhanced_data = self._add_semantic_context(normalized_data)
            
            # Generate schema markup
            schema = self._generate_schema_markup(enhanced_data)
            
            return {
                "normalized": normalized_data,
                "enhanced": enhanced_data,
                "schema": schema
            }
        except Exception as e:
            print(f"Error processing structured data: {str(e)}")
            return {"error": str(e)}
    
    def _optimize_article(self, text: str) -> str:
        """Apply article-specific optimizations."""
        # Add semantic headings
        # Enhance readability
        # Add summary and key points
        return text  # Implement optimization logic
    
    def _optimize_tutorial(self, text: str) -> str:
        """Apply tutorial-specific optimizations."""
        # Add step markers
        # Include code blocks
        # Add prerequisites
        return text  # Implement optimization logic
    
    def _optimize_documentation(self, text: str) -> str:
        """Apply documentation-specific optimizations."""
        # Add technical context
        # Include usage examples
        # Add API references
        return text  # Implement optimization logic
    
    def _optimize_general(self, text: str) -> str:
        """Apply general content optimizations."""
        # Enhance readability
        # Add semantic markers
        # Include key concepts
        return text  # Implement optimization logic
    
    def _generate_alt_text(self, caption: str, ocr_text: str) -> str:
        """Generate optimized alt text for images."""
        # Combine caption and OCR text
        # Extract key information
        # Format for accessibility
        return f"{caption} - {ocr_text[:100]}"  # Implement better logic
    
    def _extract_image_metadata(self, image: Image) -> Dict:
        """Extract and optimize image metadata."""
        return {
            "size": image.size,
            "mode": image.mode,
            "format": image.format
        }
    
    def _extract_audio_metadata(self, audio_path: str) -> Dict:
        """Extract and optimize audio metadata."""
        # Implement audio metadata extraction
        return {}
    
    def _extract_video_metadata(self, video_path: str) -> Dict:
        """Extract and optimize video metadata."""
        # Implement video metadata extraction
        return {}
    
    def _extract_key_frames(self, video_path: str) -> List[str]:
        """Extract key frames from video."""
        # Implement frame extraction
        return []
    
    def _extract_audio_track(self, video_path: str) -> str:
        """Extract audio track from video."""
        # Implement audio extraction
        return ""
    
    def _normalize_structured_data(self, data: Dict) -> Dict:
        """Normalize structured data format."""
        # Implement data normalization
        return data
    
    def _add_semantic_context(self, data: Dict) -> Dict:
        """Add semantic context to structured data."""
        # Implement semantic enhancement
        return data
    
    def _generate_schema_markup(self, data: Dict) -> Dict:
        """Generate schema.org markup."""
        # Implement schema generation
        return data

class ContentProcessor:
    """
    Process and analyze different types of content (text, images, documents, etc.)
    """
    
    def __init__(self):
        """Initialize the content processor"""
        self.supported_types = {
            'text': ['.txt', '.md', '.html'],
            'document': ['.docx', '.pdf'],
            'image': ['.jpg', '.jpeg', '.png', '.gif'],
            'audio': ['.mp3', '.wav', '.ogg'],
            'video': ['.mp4', '.avi', '.mov']
        }
    
    def process_content(
        self,
        content: Union[str, bytes, Path],
        content_type: Optional[str] = None
    ) -> Dict:
        """
        Process content and return structured data with metadata
        
        Args:
            content: Content to process (text, file path, or bytes)
            content_type: Optional content type override
            
        Returns:
            Dict containing processed content and metadata
        """
        # Determine content type if not provided
        if content_type is None:
            content_type = self._detect_content_type(content)
        
        # Process based on content type
        if content_type == 'text':
            result = self._process_text(content)
        elif content_type == 'document':
            result = self._process_document(content)
        elif content_type == 'image':
            result = self._process_image(content)
        elif content_type == 'audio':
            result = self._process_audio(content)
        elif content_type == 'video':
            result = self._process_video(content)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        # Add content_type to the result
        result["content_type"] = content_type
        return result
    
    def _detect_content_type(self, content: Union[str, bytes, Path]) -> str:
        """Detect content type using file extension or magic numbers"""
        if isinstance(content, (str, Path)):
            content_str = str(content)
            
            # Check if it's a file path
            if os.path.isfile(content_str):
                mime = magic.from_file(content_str, mime=True)
                return self._mime_to_type(mime)
            
            # Check file extension if file doesn't exist (common in tests)
            if '.' in content_str:
                ext = content_str.lower().split('.')[-1]
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
                    return 'image'
                elif ext in ['pdf', 'doc', 'docx']:
                    return 'document'
                elif ext in ['mp3', 'wav', 'm4a', 'flac']:
                    return 'audio'
                elif ext in ['mp4', 'avi', 'mov', 'mkv']:
                    return 'video'
                elif ext in ['txt', 'md', 'html', 'htm']:
                    return 'text'
            
            # Check if it's a URL
            if content_str.startswith(('http://', 'https://')):
                return 'text'
            
            # Assume it's plain text
            return 'text'
        
        elif isinstance(content, bytes):
            # Use python-magic to detect type from bytes
            mime = magic.from_buffer(content, mime=True)
            return self._mime_to_type(mime)
        
        raise ValueError("Unsupported content format")
    
    def _mime_to_type(self, mime: str) -> str:
        """Convert MIME type to content type"""
        if mime.startswith('text/'):
            return 'text'
        elif mime.startswith('image/'):
            return 'image'
        elif mime.startswith('audio/'):
            return 'audio'
        elif mime.startswith('video/'):
            return 'video'
        elif mime in ['application/pdf', 'application/msword', 
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'document'
        else:
            raise ValueError(f"Unsupported MIME type: {mime}")
    
    def _process_text(self, content: Union[str, bytes, Path]) -> Dict:
        """Process text content"""
        # Convert content to string if needed
        if isinstance(content, bytes):
            text = content.decode('utf-8')
        elif isinstance(content, Path):
            with open(content, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = str(content)
        
        # Basic text analysis
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = text.split('\n\n')
        
        # HTML processing if applicable
        is_html = False
        if text.strip().startswith('<'):
            try:
                soup = BeautifulSoup(text, 'html.parser')
                text = soup.get_text()
                is_html = True
            except:
                pass
        
        return {
            "content": text,
            "metadata": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "is_html": is_html,
                "avg_word_length": np.mean([len(word) for word in words]) if words else 0,
                "avg_sentence_length": np.mean([len(sent.split()) for sent in sentences]) if sentences else 0
            }
        }
    
    def _process_document(self, content: Union[str, bytes, Path]) -> Dict:
        """Process document content (PDF, DOCX)"""
        if isinstance(content, (str, Path)):
            file_path = str(content)
            if file_path.endswith('.pdf'):
                return self._process_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._process_docx(file_path)
        elif isinstance(content, bytes):
            # Handle PDF bytes
            if content.startswith(b'%PDF'):
                return self._process_pdf_bytes(content)
            # Handle DOCX bytes
            elif content.startswith(b'PK\x03\x04'):
                return self._process_docx_bytes(content)
        
        raise ValueError("Unsupported document format")
    
    def _process_pdf(self, file_path: str) -> Dict:
        """Process PDF file"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return self._process_text(text)
    
    def _process_pdf_bytes(self, content: bytes) -> Dict:
        """Process PDF from bytes"""
        # Save to temporary file and process
        with open('temp.pdf', 'wb') as f:
            f.write(content)
        try:
            result = self._process_pdf('temp.pdf')
        finally:
            os.remove('temp.pdf')
        return result
    
    def _process_docx(self, file_path: str) -> Dict:
        """Process DOCX file"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return self._process_text(text)
    
    def _process_docx_bytes(self, content: bytes) -> Dict:
        """Process DOCX from bytes"""
        # Save to temporary file and process
        with open('temp.docx', 'wb') as f:
            f.write(content)
        try:
            result = self._process_docx('temp.docx')
        finally:
            os.remove('temp.docx')
        return result
    
    def _process_image(self, content: Union[str, bytes, Path]) -> Dict:
        """Process image content"""
        if isinstance(content, (str, Path)):
            image = Image.open(str(content))
        else:
            image = Image.open(io.BytesIO(content))
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        
        # Get image metadata
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height
        }
        
        return {
            "content": text,
            "metadata": metadata
        }
    
    def _process_audio(self, content: Union[str, bytes, Path]) -> Dict:
        """Process audio content"""
        # This is a placeholder for audio processing
        # In a real implementation, this would use libraries like librosa
        # to analyze audio content
        return {
            "content": "",
            "metadata": {
                "type": "audio",
                "status": "not_implemented"
            }
        }
    
    def _process_video(self, content: Union[str, bytes, Path]) -> Dict:
        """Process video content"""
        # This is a placeholder for video processing
        # In a real implementation, this would use libraries like opencv
        # to analyze video content
        return {
            "content": "",
            "metadata": {
                "type": "video",
                "status": "not_implemented"
            }
        }
    
    def extract_metadata(self, content: Union[str, bytes, Path]) -> Dict:
        """Extract metadata from content"""
        processed = self.process_content(content)
        return processed["metadata"]
    
    def get_content_type(self, content: Union[str, bytes, Path]) -> str:
        """Get content type"""
        return self._detect_content_type(content)
    
    def is_supported_type(self, content_type: str) -> bool:
        """Check if content type is supported"""
        return content_type in self.supported_types 