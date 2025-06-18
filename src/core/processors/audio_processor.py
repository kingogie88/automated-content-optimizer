import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Dict, Optional, List
import logging
from dataclasses import dataclass

@dataclass
class AudioMetadata:
    duration: float
    sample_rate: int
    channels: int
    format: str
    size_mb: float
    segments: List[Dict]

class AudioProcessor:
    def __init__(self):
        self.logger = logging.getLogger("audio_processor")
    
    async def process_audio(self, audio_path: str) -> Dict:
        """Process audio file and extract metadata and features."""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path)
            
            # Extract metadata
            metadata = await self._extract_metadata(audio_path, y, sr)
            
            # Perform audio segmentation
            segments = await self._segment_audio(y, sr)
            metadata.segments = segments
            
            # Extract features
            features = await self._extract_features(y, sr)
            
            return {
                "metadata": self._metadata_to_dict(metadata),
                "features": features
            }
            
        except Exception as e:
            self.logger.error(f"Error processing audio {audio_path}: {str(e)}")
            raise
    
    async def _extract_metadata(self, audio_path: str, y: np.ndarray, sr: int) -> AudioMetadata:
        """Extract audio metadata."""
        try:
            audio_file = Path(audio_path)
            
            # Get audio info using soundfile
            with sf.SoundFile(audio_path) as f:
                channels = f.channels
                format_name = f.format
            
            metadata = AudioMetadata(
                duration=librosa.get_duration(y=y, sr=sr),
                sample_rate=sr,
                channels=channels,
                format=format_name,
                size_mb=audio_file.stat().st_size / (1024 * 1024),
                segments=[]
            )
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {str(e)}")
            raise
    
    async def _segment_audio(self, y: np.ndarray, sr: int) -> List[Dict]:
        """Segment audio into speech/music/silence."""
        try:
            segments = []
            
            # Detect silence
            non_silent_intervals = librosa.effects.split(
                y,
                top_db=30,
                frame_length=2048,
                hop_length=512
            )
            
            for i, (start, end) in enumerate(non_silent_intervals):
                # Convert frame indices to time
                start_time = librosa.frames_to_time(start, sr=sr)
                end_time = librosa.frames_to_time(end, sr=sr)
                
                # Extract segment features
                segment = y[start:end]
                
                # Classify segment (basic implementation)
                segment_type = self._classify_segment(segment, sr)
                
                segments.append({
                    "id": i,
                    "start": float(start_time),
                    "end": float(end_time),
                    "type": segment_type
                })
            
            return segments
            
        except Exception as e:
            self.logger.error(f"Error segmenting audio: {str(e)}")
            raise
    
    async def _extract_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract audio features."""
        try:
            # Compute mel spectrogram
            mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
            mel_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Compute MFCC
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Compute chromagram
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            # Compute onset strength
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
            
            return {
                "tempo": float(tempo[0]),
                "mean_mfcc": mfcc.mean(axis=1).tolist(),
                "mean_chroma": chroma.mean(axis=1).tolist(),
                "spectral_contrast": librosa.feature.spectral_contrast(y=y, sr=sr).mean(axis=1).tolist()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting features: {str(e)}")
            raise
    
    def _classify_segment(self, segment: np.ndarray, sr: int) -> str:
        """Basic segment classification."""
        # Simple classification based on spectral centroid
        centroid = librosa.feature.spectral_centroid(y=segment, sr=sr).mean()
        
        if centroid > 2000:
            return "music"
        elif centroid > 1000:
            return "speech"
        else:
            return "noise"
    
    def _metadata_to_dict(self, metadata: AudioMetadata) -> Dict:
        """Convert metadata to dictionary format."""
        return {
            "duration": metadata.duration,
            "sample_rate": metadata.sample_rate,
            "channels": metadata.channels,
            "format": metadata.format,
            "size_mb": metadata.size_mb,
            "segments": metadata.segments
        } 