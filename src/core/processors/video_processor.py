import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import json
from dataclasses import dataclass
import logging
from moviepy.editor import VideoFileClip
import tempfile

@dataclass
class VideoMetadata:
    duration: float
    fps: float
    resolution: tuple
    format: str
    size_mb: float
    has_audio: bool
    key_frames: List[str]

class VideoProcessor:
    def __init__(self, temp_dir: Optional[str] = None):
        self.logger = logging.getLogger("video_processor")
        self.temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.gettempdir())
        self.temp_dir.mkdir(exist_ok=True)
    
    async def process_video(self, video_path: str) -> Dict:
        """Process video file and extract metadata, frames, and audio."""
        try:
            # Extract metadata
            metadata = await self._extract_metadata(video_path)
            
            # Extract key frames
            key_frames = await self._extract_key_frames(video_path)
            metadata.key_frames = key_frames
            
            # Extract audio if present
            if metadata.has_audio:
                audio_path = await self._extract_audio(video_path)
            else:
                audio_path = None
            
            return {
                "metadata": self._metadata_to_dict(metadata),
                "audio_path": str(audio_path) if audio_path else None,
                "key_frames": key_frames
            }
            
        except Exception as e:
            self.logger.error(f"Error processing video {video_path}: {str(e)}")
            raise
    
    async def _extract_metadata(self, video_path: str) -> VideoMetadata:
        """Extract video metadata."""
        try:
            cap = cv2.VideoCapture(video_path)
            video_file = Path(video_path)
            
            # Get basic properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Calculate duration
            duration = frame_count / fps if fps > 0 else 0
            
            # Check for audio using moviepy
            with VideoFileClip(video_path) as video:
                has_audio = video.audio is not None
            
            metadata = VideoMetadata(
                duration=duration,
                fps=fps,
                resolution=(width, height),
                format=video_file.suffix.lower()[1:],
                size_mb=video_file.stat().st_size / (1024 * 1024),
                has_audio=has_audio,
                key_frames=[]
            )
            
            cap.release()
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {str(e)}")
            raise
    
    async def _extract_key_frames(self, video_path: str) -> List[str]:
        """Extract key frames from video using scene detection."""
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            
            ret, prev_frame = cap.read()
            if not ret:
                return frames
            
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            frame_count = 0
            
            while True:
                ret, curr_frame = cap.read()
                if not ret:
                    break
                
                # Process every 30th frame or when significant change is detected
                if frame_count % 30 == 0:
                    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
                    
                    # Calculate frame difference
                    diff = cv2.absdiff(curr_gray, prev_gray)
                    mean_diff = np.mean(diff)
                    
                    # If significant change detected, save frame
                    if mean_diff > 30:  # Threshold for change detection
                        frame_path = self.temp_dir / f"frame_{frame_count}.jpg"
                        cv2.imwrite(str(frame_path), curr_frame)
                        frames.append(str(frame_path))
                    
                    prev_gray = curr_gray
                
                frame_count += 1
            
            cap.release()
            return frames
            
        except Exception as e:
            self.logger.error(f"Error extracting key frames: {str(e)}")
            raise
    
    async def _extract_audio(self, video_path: str) -> Optional[Path]:
        """Extract audio track from video."""
        try:
            video = VideoFileClip(video_path)
            if video.audio is None:
                return None
            
            audio_path = self.temp_dir / f"{Path(video_path).stem}_audio.wav"
            video.audio.write_audiofile(str(audio_path))
            
            video.close()
            return audio_path
            
        except Exception as e:
            self.logger.error(f"Error extracting audio: {str(e)}")
            raise
    
    def _metadata_to_dict(self, metadata: VideoMetadata) -> Dict:
        """Convert metadata to dictionary format."""
        return {
            "duration": metadata.duration,
            "fps": metadata.fps,
            "resolution": {
                "width": metadata.resolution[0],
                "height": metadata.resolution[1]
            },
            "format": metadata.format,
            "size_mb": metadata.size_mb,
            "has_audio": metadata.has_audio
        } 