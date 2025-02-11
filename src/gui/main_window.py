"""
Main application window for the Sales Conversation Transcription System.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar,
    QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from src.transcription import AudioTranscriber, AudioProcessor, SpeakerClassifier
from src.gui.transcription_view import TranscriptionView
from src.gui.timeline_view import TimelineView
from config import SUPPORTED_FORMATS

class TranscriptionWorker(QThread):
    """Worker thread for handling transcription processing."""
    progress = pyqtSignal(float)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, audio_path: Path):
        super().__init__()
        self.audio_path = audio_path
        self.transcriber = AudioTranscriber()
        self.processor = AudioProcessor()
        self.classifier = SpeakerClassifier()
        
    def run(self):
        try:
            # Validate file
            valid, error = self.processor.validate_file(self.audio_path)
            if not valid:
                self.error.emit(error)
                return
                
            # Preprocess audio
            processed_path = self.processor.preprocess_audio(self.audio_path)
            
            # Transcribe audio
            transcription = self.transcriber.transcribe(processed_path)
            
            # Classify speakers
            segments = self.classifier.classify_segments(transcription["segments"])
            
            # Detect overlaps
            segments = self.classifier.detect_speaker_overlap(segments)
            
            # Get statistics
            stats = self.classifier.get_speaker_statistics(segments)
            
            # Prepare results
            results = {
                "segments": segments,
                "statistics": stats,
                "language": transcription["language"],
                "duration": transcription["duration"]
            }
            
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.processor.cleanup()

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Conversation Transcription System")
        self.setMinimumSize(1024, 768)
        
        # Initialize UI
        self._init_ui()
        
        # Initialize state
        self.current_file = None
        self.worker = None
        
    def _init_ui(self):
        """Initialize the user interface."""
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add toolbar
        toolbar = QHBoxLayout()
        layout.addLayout(toolbar)
        
        # Add file selection button
        self.file_btn = QPushButton("Select Audio File")
        self.file_btn.clicked.connect(self._select_file)
        toolbar.addWidget(self.file_btn)
        
        # Add process button
        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self._start_processing)
        self.process_btn.setEnabled(False)
        toolbar.addWidget(self.process_btn)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        toolbar.addWidget(self.progress_bar)
        
        toolbar.addStretch()
        
        # Add views
        views_layout = QHBoxLayout()
        layout.addLayout(views_layout)
        
        # Add transcription view
        self.transcription_view = TranscriptionView()
        views_layout.addWidget(self.transcription_view)
        
        # Add timeline view
        self.timeline_view = TimelineView()
        views_layout.addWidget(self.timeline_view)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def _select_file(self):
        """Handle file selection."""
        formats = " ".join(f"*{fmt}" for fmt in SUPPORTED_FORMATS)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            f"Audio Files ({formats})"
        )
        
        if file_path:
            self.current_file = Path(file_path)
            self.process_btn.setEnabled(True)
            self.status_bar.showMessage(f"Selected file: {self.current_file.name}")
            
    def _start_processing(self):
        """Start audio processing."""
        if not self.current_file:
            return
            
        # Disable controls
        self.file_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
        
        # Show progress
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        
        # Create and start worker
        self.worker = TranscriptionWorker(self.current_file)
        self.worker.progress.connect(self._update_progress)
        self.worker.finished.connect(self._processing_finished)
        self.worker.error.connect(self._processing_error)
        self.worker.start()
        
    def _update_progress(self, value):
        """Update progress bar."""
        self.progress_bar.setValue(int(value))
        
    def _processing_finished(self, results):
        """Handle completed processing."""
        # Re-enable controls
        self.file_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.progress_bar.hide()
        
        # Update views
        self.transcription_view.set_results(results)
        self.timeline_view.set_results(results)
        
        # Update status
        duration = int(results["duration"])
        self.status_bar.showMessage(
            f"Processing complete - Duration: {duration//60}:{duration%60:02d}"
        )
        
    def _processing_error(self, error):
        """Handle processing error."""
        # Re-enable controls
        self.file_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.progress_bar.hide()
        
        # Show error
        QMessageBox.critical(self, "Error", str(error))
        self.status_bar.showMessage("Error during processing")