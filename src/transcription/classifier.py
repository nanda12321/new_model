"""
Handles speaker classification in transcribed audio.
"""

import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from transformers import pipeline

from config import (
    SPEAKER_CLASSES,
    CLASSIFICATION_CONFIDENCE_THRESHOLD,
    MIN_SEGMENT_LENGTH,
    DEVICE
)

class SpeakerClassifier:
    """Handles speaker classification in transcribed segments."""
    
    def __init__(self):
        """Initialize the speaker classifier."""
        # Load pretrained text classification model
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            device=0 if DEVICE == "cuda" else -1
        )
        
    def classify_segments(self, segments: List[Dict]) -> List[Dict]:
        """
        Classify speakers in transcribed segments.
        
        Args:
            segments: List of transcription segments
            
        Returns:
            List of segments with speaker labels
        """
        classified_segments = []
        
        for segment in segments:
            # Skip segments shorter than minimum length
            duration = segment["end"] - segment["start"]
            if duration < MIN_SEGMENT_LENGTH:
                continue
                
            # Classify speaker
            result = self.classifier(segment["text"])[0]
            confidence = result["score"]
            
            # Only include classifications above threshold
            if confidence >= CLASSIFICATION_CONFIDENCE_THRESHOLD:
                segment["speaker"] = result["label"]
                segment["speaker_confidence"] = confidence
                classified_segments.append(segment)
            
        return classified_segments
        
    def detect_speaker_overlap(self, segments: List[Dict]) -> List[Dict]:
        """
        Detect and mark potential speaker overlaps.
        
        Args:
            segments: List of classified segments
            
        Returns:
            List of segments with overlap information
        """
        for i in range(len(segments)-1):
            current = segments[i]
            next_seg = segments[i+1]
            
            # Check for temporal overlap
            if current["end"] > next_seg["start"]:
                overlap_duration = current["end"] - next_seg["start"]
                current["overlap"] = {
                    "duration": overlap_duration,
                    "overlaps_with": i + 1
                }
                next_seg["overlap"] = {
                    "duration": overlap_duration,
                    "overlaps_with": i
                }
                
        return segments
        
    def get_speaker_statistics(self, segments: List[Dict]) -> Dict:
        """
        Calculate statistics about speaker participation.
        
        Args:
            segments: List of classified segments
            
        Returns:
            Dictionary containing speaker statistics
        """
        stats = {speaker: {
            "total_time": 0.0,
            "segment_count": 0,
            "word_count": 0
        } for speaker in SPEAKER_CLASSES}
        
        for segment in segments:
            if "speaker" in segment:
                speaker = segment["speaker"]
                duration = segment["end"] - segment["start"]
                stats[speaker]["total_time"] += duration
                stats[speaker]["segment_count"] += 1
                stats[speaker]["word_count"] += len(segment["text"].split())
                
        return stats