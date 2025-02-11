"""
Utilities for audio file handling.
"""

import soundfile as sf
from pathlib import Path
from typing import Dict, Tuple

from config import SUPPORTED_FORMATS, MAX_FILE_SIZE, MIN_SAMPLE_RATE

def validate_audio_file(file_path: Path) -> Tuple[bool, str]:
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

def get_audio_info(file_path: Path) -> Dict:
    """
    Get audio file information.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary containing audio information
    """
    info = sf.info(file_path)
    return {
        "samplerate": info.samplerate,
        "channels": info.channels,
        "duration": info.duration,
        "format": info.format,
        "size_mb": file_path.stat().st_size / (1024 * 1024)
    }