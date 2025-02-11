"""
Widget for displaying conversation timeline.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor

class TimelineView(QWidget):
    """Widget for displaying conversation timeline visualization."""
    
    def __init__(self):
        super().__init__()
        self.results = None
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create graphics view
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        layout.addWidget(self.view)
        
        # Set up colors
        self.colors = {
            "salesperson": QColor("#4CAF50"),
            "customer": QColor("#2196F3")
        }
        
    def set_results(self, results):
        """
        Set and display timeline results.
        
        Args:
            results: Dictionary containing transcription results
        """
        self.results = results
        self._update_display()
        
    def _update_display(self):
        """Update the timeline display."""
        if not self.results:
            return
            
        self.scene.clear()
        
        # Calculate dimensions
        duration = self.results["duration"]
        height = 100
        width = max(self.width() - 20, 600)
        scale = width / duration
        
        # Draw timeline base
        self.scene.addLine(0, height/2, width, height/2, QPen(Qt.GlobalColor.gray))
        
        # Draw segments
        for segment in self.results["segments"]:
            if "speaker" not in segment:
                continue
                
            x = segment["start"] * scale
            w = (segment["end"] - segment["start"]) * scale
            y = height/4 if segment["speaker"] == "salesperson" else height/2
            
            # Draw segment block
            rect = self.scene.addRect(
                x, y, w, height/4,
                QPen(self.colors[segment["speaker"]]),
                QBrush(self.colors[segment["speaker"]].lighter())
            )
            
            # Add overlap indicator if present
            if "overlap" in segment:
                self.scene.addRect(
                    x + w - 5, y, 5, height/4,
                    QPen(Qt.GlobalColor.red),
                    QBrush(Qt.GlobalColor.red)
                )
                
        # Update view
        self.view.setSceneRect(QRectF(0, 0, width, height))
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        if self.results:
            self._update_display()