# Audio Transcription Project

This project provides a GUI application for audio transcription and speaker classification using Whisper and transformer models.

## System Requirements

- Python 3.8 or higher
- Minimum RAM: System will check for sufficient memory
- Storage Space: System will verify available disk space
- GPU: Optional but recommended for better performance (CUDA compatible)

## Dependencies

The following Python packages are required:
```
torch>=2.0.0
openai-whisper>=20231117
numpy>=1.24.0
pandas>=2.0.0
soundfile>=0.12.1
librosa>=0.10.1
PyQt6>=6.5.0
transformers>=4.30.0
pyaudioanalysis>=0.3.14
scipy>=1.10.1
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python src/main.py
```

2. The application will:
   - Check system requirements
   - Initialize required directories
   - Download necessary models (first run only):
     - Whisper model for audio transcription
     - Speaker classification model
   - Launch the GUI interface

3. Using the GUI:
   - The application will open a window interface
   - Follow the on-screen instructions for:
     - Loading audio files
     - Running transcription
     - Performing speaker classification

## Notes

- First run may take longer due to model downloads
- GPU acceleration will be automatically used if available
- Temporary files and models are stored in designated directories

## Troubleshooting

If you encounter any errors:
1. Ensure all system requirements are met
2. Verify that all dependencies are properly installed
3. Check console output for specific error messages
4. Ensure sufficient disk space for model downloads

For additional support, please refer to the project's issue tracker.