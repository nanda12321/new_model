"""
Handles audio transcription using Whisper model.
"""

import os
import torch
import whisper
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from config import WHISPER_MODEL, DEVICE, MIN_SAMPLE_RATE

class AudioTranscriber:
    """Handles audio transcription using the Whisper model."""
    
    def __init__(self):
        """Initialize the transcriber with Whisper model."""
        self.model = whisper.load_model(WHISPER_MODEL, device=DEVICE)
        self.audio_duration = 0
        
    def transcribe(self, audio_path: Path) -> Dict:
        """
        Transcribe audio file using Whisper model.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription segments with timestamps
        """
        try:
            # Load and process audio
            audio = whisper.load_audio(str(audio_path))
            self.audio_duration = len(audio) / MIN_SAMPLE_RATE
            
            # Perform transcription
            result = self.model.transcribe(
                audio,
                task="transcribe",
                fp16=torch.cuda.is_available(),
                language=None,  # Auto-detect language
                verbose=False
            )
            
            # Process and format results
            processed_segments = []
            for segment in result["segments"]:
                processed_segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "confidence": float(segment["confidence"])
                })
            
            return {
                "segments": processed_segments,
                "language": result["language"],
                "duration": self.audio_duration
            }
            
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
            
    def get_processing_progress(self) -> float:
        """Get the current processing progress as a percentage."""
        if not self.audio_duration:
            return 0.0
        # Progress estimation based on Whisper's processing
        return min(100.0, (self.model._progress * 100) / self.audio_duration)