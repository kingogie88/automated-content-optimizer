import pytest
import numpy as np
from pathlib import Path
import tempfile
import cv2
import librosa
import soundfile as sf
from PIL import Image

from src.core.processors.video_processor import VideoProcessor
from src.core.processors.audio_processor import AudioProcessor

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def sample_video(temp_dir):
    """Create a sample video file for testing."""
    video_path = Path(temp_dir) / "test_video.mp4"
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(video_path), fourcc, 30.0, (640,480))
    
    # Generate some frames
    for _ in range(90):  # 3 seconds at 30 fps
        frame = np.random.randint(0, 255, (480,640,3), dtype=np.uint8)
        out.write(frame)
    
    out.release()
    return str(video_path)

@pytest.fixture
def sample_audio(temp_dir):
    """Create a sample audio file for testing."""
    audio_path = Path(temp_dir) / "test_audio.wav"
    
    # Generate a simple sine wave
    sr = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(sr * duration))
    y = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Save audio file
    sf.write(str(audio_path), y, sr)
    return str(audio_path)

class TestVideoProcessor:
    @pytest.mark.asyncio
    async def test_video_metadata_extraction(self, sample_video):
        """Test video metadata extraction."""
        processor = VideoProcessor()
        result = await processor.process_video(sample_video)
        
        assert "metadata" in result
        metadata = result["metadata"]
        assert isinstance(metadata["duration"], float)
        assert isinstance(metadata["fps"], float)
        assert "width" in metadata["resolution"]
        assert "height" in metadata["resolution"]
        assert isinstance(metadata["size_mb"], float)
        assert isinstance(metadata["has_audio"], bool)
    
    @pytest.mark.asyncio
    async def test_key_frame_extraction(self, sample_video):
        """Test key frame extraction."""
        processor = VideoProcessor()
        result = await processor.process_video(sample_video)
        
        assert "key_frames" in result
        assert isinstance(result["key_frames"], list)
        
        # Check if key frames are valid image files
        for frame_path in result["key_frames"]:
            assert Path(frame_path).exists()
            img = Image.open(frame_path)
            assert img.size == (640, 480)

class TestAudioProcessor:
    @pytest.mark.asyncio
    async def test_audio_metadata_extraction(self, sample_audio):
        """Test audio metadata extraction."""
        processor = AudioProcessor()
        result = await processor.process_audio(sample_audio)
        
        assert "metadata" in result
        metadata = result["metadata"]
        assert isinstance(metadata["duration"], float)
        assert isinstance(metadata["sample_rate"], int)
        assert isinstance(metadata["channels"], int)
        assert isinstance(metadata["format"], str)
        assert isinstance(metadata["size_mb"], float)
    
    @pytest.mark.asyncio
    async def test_audio_feature_extraction(self, sample_audio):
        """Test audio feature extraction."""
        processor = AudioProcessor()
        result = await processor.process_audio(sample_audio)
        
        assert "features" in result
        features = result["features"]
        assert "tempo" in features
        assert "mean_mfcc" in features
        assert "mean_chroma" in features
        assert "spectral_contrast" in features
    
    @pytest.mark.asyncio
    async def test_audio_segmentation(self, sample_audio):
        """Test audio segmentation."""
        processor = AudioProcessor()
        result = await processor.process_audio(sample_audio)
        
        assert "metadata" in result
        metadata = result["metadata"]
        assert "segments" in metadata
        
        segments = metadata["segments"]
        assert isinstance(segments, list)
        
        if segments:  # If any segments were detected
            segment = segments[0]
            assert "id" in segment
            assert "start" in segment
            assert "end" in segment
            assert "type" in segment
            assert segment["type"] in ["speech", "music", "noise"] 