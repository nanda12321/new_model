"""
Error handling utilities.
"""

import sys
import traceback
from typing import Optional, Callable
from PyQt6.QtWidgets import QMessageBox

class ErrorHandler:
    """Global error handler for the application."""
    
    @staticmethod
    def handle_error(error: Exception, parent=None, callback: Optional[Callable] = None):
        """
        Handle application errors.
        
        Args:
            error: The exception to handle
            parent: Parent widget for displaying error messages
            callback: Optional callback to execute after error handling
        """
        # Get error details
        error_type = type(error).__name__
        error_message = str(error)
        error_trace = "".join(traceback.format_tb(error.__traceback__))
        
        # Log error
        print(f"Error: {error_type}: {error_message}", file=sys.stderr)
        print("Traceback:", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        
        # Show error dialog if parent is provided
        if parent:
            QMessageBox.critical(
                parent,
                "Error",
                f"{error_type}: {error_message}\n\nPlease check the logs for details."
            )
        
        # Execute callback if provided
        if callback:
            try:
                callback()
            except Exception as e:
                print(f"Error in error handler callback: {str(e)}", file=sys.stderr)
                
    @staticmethod
    def show_warning(message: str, parent=None):
        """
        Show warning message.
        
        Args:
            message: Warning message to display
            parent: Parent widget for displaying warning
        """
        if parent:
            QMessageBox.warning(parent, "Warning", message)
        else:
            print(f"Warning: {message}", file=sys.stderr)