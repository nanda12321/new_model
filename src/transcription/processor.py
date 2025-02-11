"""
Handles audio preprocessing and validation.
"""

import os
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Dict, Tuple

from config import (
    SUPPORTED_FORMATS,
    MAX_FILE_SIZE,
    MIN_SAMPLE_RATE,
    TEMP_DIR
)

class AudioProcessor:
    """Handles audio file preprocessing and validation."""
    
    def __init__(self):
        """Initialize the audio processor."""
        self.temp_dir = TEMP_DIR
        
    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate audio file meets requirements.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file exists
        if not file_path.exists():
            return False, "File does not exist"
            
        # Check file format
        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            return False, f"Unsupported format. Must be one of: {SUPPORTED_FORMATS}"
            
        # Check file size
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return False, f"File too large. Maximum size: {MAX_FILE_SIZE/1024/1024}MB"
            
        try:
            # Check audio properties
            info = sf.info(file_path)
            if info.samplerate < MIN_SAMPLE_RATE:
                return False, f"Sample rate too low. Minimum: {MIN_SAMPLE_RATE}Hz"
                
        except Exception as e:
            return False, f"Invalid audio file: {str(e)}"
            
        return True, ""
        
    def preprocess_audio(self, file_path: Path) -> Path:
        """
        Preprocess audio file for optimal transcription.
        
        Args:
            file_path: Path to input audio file
            
        Returns:
            Path to processed audio file
        """
        # Load audio
        audio, sr = librosa.load(file_path, sr=None)
        
        # Resample if needed
        if sr != MIN_SAMPLE_RATE:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=MIN_SAMPLE_RATE)
            sr = MIN_SAMPLE_RATE
            
        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio)
            
        # Normalize audio
        audio = librosa.util.normalize(audio)
            
        # Save processed file
        output_path = self.temp_dir / f"processed_{file_path.name}"
        sf.write(output_path, audio, sr)
        
        return output_path
        
    def cleanup(self):
        """Clean up temporary files."""
        for file in self.temp_dir.glob("processed_*"):
            try:
                file.unlink()
            except Exception:
                pass