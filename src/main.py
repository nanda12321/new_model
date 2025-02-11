"""
Main entry point for the Sales Conversation Transcription System.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.gui import MainWindow
from config import BASE_DIR, MODELS_DIR, OUTPUT_DIR, TEMP_DIR

def check_system_requirements():
    """Verify that the system meets minimum requirements."""
    import psutil
    import torch
    
    # Check RAM
    available_ram = psutil.virtual_memory().total
    if available_ram < MIN_RAM:
        raise RuntimeError(f"Insufficient RAM. Required: {MIN_RAM/1024/1024/1024:.1f}GB, Available: {available_ram/1024/1024/1024:.1f}GB")
    
    # Check storage
    free_storage = psutil.disk_usage(BASE_DIR).free
    if free_storage < MIN_STORAGE:
        raise RuntimeError(f"Insufficient storage space. Required: {MIN_STORAGE/1024/1024/1024:.1f}GB, Available: {free_storage/1024/1024/1024:.1f}GB")
    
    # Check GPU
    if torch.cuda.is_available():
        gpu_info = torch.cuda.get_device_properties(0)
        print(f"GPU detected: {gpu_info.name} ({gpu_info.total_memory/1024/1024/1024:.1f}GB)")
    else:
        print("No GPU detected. Using CPU for processing.")
        
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or higher is required")
        
    return True

def initialize_application():
    """Initialize application directories and resources."""
    try:
        # Create required directories
        for directory in [MODELS_DIR, OUTPUT_DIR, TEMP_DIR]:
            directory.mkdir(exist_ok=True)
            
        # Download Whisper model if not exists
        model_path = MODELS_DIR / WHISPER_MODEL
        if not model_path.exists():
            print(f"Downloading Whisper model '{WHISPER_MODEL}'...")
            import whisper
            whisper.load_model(WHISPER_MODEL, download_root=str(MODELS_DIR))
            
        # Initialize speaker classification model
        classifier_path = MODELS_DIR / "speaker_classifier"
        if not classifier_path.exists():
            print("Downloading speaker classification model...")
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
            tokenizer.save_pretrained(classifier_path)
            model.save_pretrained(classifier_path)
            
        print("Application initialized successfully.")
        return True
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        return False

def main():
    """Main application entry point."""
    try:
        # Check system requirements
        check_system_requirements()
        
        # Initialize application
        initialize_application()
        
        # Start GUI
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()