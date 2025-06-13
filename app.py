import os
import gradio as gr
from ui.app import create_geo_interface
from dotenv import load_dotenv
import tempfile
import os
from pathlib import Path
from src.core.processors.video_processor import VideoProcessor
from src.core.processors.audio_processor import AudioProcessor
import asyncio
import json

# Load environment variables
load_dotenv()

# Validate required environment variables
required_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# Create and launch the interface
app = create_geo_interface()

# Initialize processors
video_processor = VideoProcessor()
audio_processor = AudioProcessor()

def process_video(video_path):
    """Process video file and return results."""
    try:
        # Run video processing in async context
        result = asyncio.run(video_processor.process_video(video_path))
        
        # Format results for display
        metadata = result["metadata"]
        key_frames = result["key_frames"]
        
        # Create a formatted output
        output = f"""
        ## Video Analysis Results

        ### Metadata
        - Duration: {metadata['duration']:.2f} seconds
        - FPS: {metadata['fps']:.2f}
        - Resolution: {metadata['resolution']['width']}x{metadata['resolution']['height']}
        - Format: {metadata['format']}
        - Size: {metadata['size_mb']:.2f} MB
        - Has Audio: {'Yes' if metadata['has_audio'] else 'No'}

        ### Key Frames
        - Number of key frames: {len(key_frames)}
        """
        
        return output, key_frames
        
    except Exception as e:
        return f"Error processing video: {str(e)}", []

def process_audio(audio_path):
    """Process audio file and return results."""
    try:
        # Run audio processing in async context
        result = asyncio.run(audio_processor.process_audio(audio_path))
        
        # Format results for display
        metadata = result["metadata"]
        features = result["features"]
        
        # Create a formatted output
        output = f"""
        ## Audio Analysis Results

        ### Metadata
        - Duration: {metadata['duration']:.2f} seconds
        - Sample Rate: {metadata['sample_rate']} Hz
        - Channels: {metadata['channels']}
        - Format: {metadata['format']}
        - Size: {metadata['size_mb']:.2f} MB

        ### Features
        - Tempo: {features['tempo']:.2f} BPM
        - Number of segments: {len(metadata['segments'])}

        ### Segments
        """
        
        # Add segment information
        for segment in metadata['segments']:
            output += f"""
        - Segment {segment['id']}:
          - Type: {segment['type']}
          - Start: {segment['start']:.2f}s
          - End: {segment['end']:.2f}s
            """
        
        return output
        
    except Exception as e:
        return f"Error processing audio: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Content Optimizer") as demo:
    gr.Markdown("# Automated Content Optimizer")
    gr.Markdown("Upload media files for analysis and optimization.")
    
    with gr.Tab("Video Processing"):
        with gr.Row():
            video_input = gr.Video(label="Upload Video")
            with gr.Column():
                video_output = gr.Markdown(label="Analysis Results")
                frames_gallery = gr.Gallery(label="Key Frames", show_label=True)
        video_button = gr.Button("Process Video")
        video_button.click(
            fn=process_video,
            inputs=video_input,
            outputs=[video_output, frames_gallery]
        )
    
    with gr.Tab("Audio Processing"):
        with gr.Row():
            audio_input = gr.Audio(label="Upload Audio")
            audio_output = gr.Markdown(label="Analysis Results")
        audio_button = gr.Button("Process Audio")
        audio_button.click(
            fn=process_audio,
            inputs=audio_input,
            outputs=audio_output
        )
    
    gr.Markdown("""
    ## Features
    - Video analysis with key frame extraction
    - Audio processing with segment detection
    - Detailed metadata extraction
    - Feature analysis
    
    ## Notes
    - Supported video formats: MP4, AVI, MOV
    - Supported audio formats: WAV, MP3, OGG
    - Maximum file size: 50MB
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch() 