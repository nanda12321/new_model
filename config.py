"""
Configuration settings for the Sales Conversation Transcription System.
"""

import os
from pathlib import Path
import torch

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Create necessary directories
for directory in [MODELS_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Audio processing settings
SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a']
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
MIN_SAMPLE_RATE = 16000
MIN_SEGMENT_LENGTH = 2  # seconds

# Whisper model settings
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Speaker classification settings
SPEAKER_CLASSES = ["salesperson", "customer"]
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.75

# Export settings
EXPORT_FORMATS = ["txt", "csv", "json"]

# Performance settings
BATCH_SIZE = 16
NUM_WORKERS = os.cpu_count() or 2

# System requirements
MIN_RAM = 8 * 1024 * 1024 * 1024  # 8GB in bytes
MIN_STORAGE = 5 * 1024 * 1024 * 1024  # 5GB in bytes