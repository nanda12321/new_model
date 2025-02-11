"""
Widget for displaying transcription results.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QComboBox,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox
)
from pathlib import Path
from src.utils.export_utils import export_transcript
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor

class TranscriptionView(QWidget):
    """Widget for displaying and interacting with transcription results."""
    
    def __init__(self):
        super().__init__()
        self.results = None
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Add toolbar
        toolbar = QHBoxLayout()
        layout.addLayout(toolbar)
        
        # Add filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Speakers", "Salesperson", "Customer"])
        self.filter_combo.currentTextChanged.connect(self._filter_changed)
        toolbar.addWidget(self.filter_combo)
        
        # Add export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self._export_transcript)
        toolbar.addWidget(export_btn)
        
        toolbar.addStretch()
        
        # Add transcript display
        self.transcript = QTextEdit()
        self.transcript.setReadOnly(True)
        layout.addWidget(self.transcript)
        
    def set_results(self, results):
        """
        Set and display transcription results.
        
        Args:
            results: Dictionary containing transcription results
        """
        self.results = results
        self._update_display()
        
    def _update_display(self):
        """Update the transcript display."""
        if not self.results:
            return
            
        self.transcript.clear()
        cursor = self.transcript.textCursor()
        
        # Format for timestamps
        time_format = QTextCharFormat()
        time_format.setForeground(QColor("gray"))
        
        # Format for speakers
        speaker_formats = {
            "salesperson": QTextCharFormat(),
            "customer": QTextCharFormat()
        }
        speaker_formats["salesperson"].setBackground(QColor("#E8F5E9"))
        speaker_formats["customer"].setBackground(QColor("#E3F2FD"))
        
        filter_text = self.filter_combo.currentText().lower()
        
        for segment in self.results["segments"]:
            if filter_text != "all speakers" and segment["speaker"] != filter_text:
                continue
                
            # Add timestamp
            cursor.insertText(
                f"[{int(segment['start'])//60}:{int(segment['start'])%60:02d}] ",
                time_format
            )
            
            # Add speaker and text
            speaker_format = speaker_formats.get(segment["speaker"], QTextCharFormat())
            cursor.insertText(
                f"{segment['speaker'].title()}: {segment['text']}\n",
                speaker_format
            )
            
    def _filter_changed(self, filter_text):
        """Handle filter changes."""
        self._update_display()
        
    def _export_transcript(self):
        """Export transcript to file."""
        if not self.results:
            return
            
        # Create file dialog
        file_path, selected_format = QFileDialog.getSaveFileName(
            self,
            "Export Transcript",
            "",
            "Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if not file_path:
            return
            
        try:
            # Determine format from selected filter
            format = "txt"
            if file_path.endswith(".csv"):
                format = "csv"
            elif file_path.endswith(".json"):
                format = "json"
                
            # Export using utility function
            export_transcript(self.results, Path(file_path), format)
            
            # Show success message
            QMessageBox.information(
                self,
                "Export Complete",
                f"Transcript exported successfully to {file_path}"
            )
            
        except Exception as e:
            # Show error message
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export transcript: {str(e)}"
            )