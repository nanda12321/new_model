"""
Utilities for exporting transcription results.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List

def export_transcript(results: Dict, output_path: Path, format: str = "txt"):
    """
    Export transcription results to file.
    
    Args:
        results: Dictionary containing transcription results
        output_path: Path to save the export
        format: Export format (txt, csv, or json)
    """
    if format == "txt":
        _export_txt(results, output_path)
    elif format == "csv":
        _export_csv(results, output_path)
    elif format == "json":
        _export_json(results, output_path)
    else:
        raise ValueError(f"Unsupported export format: {format}")

def _export_txt(results: Dict, output_path: Path):
    """Export results as formatted text file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("Sales Conversation Transcript\n")
        f.write("="*30 + "\n\n")
        
        # Write segments
        for segment in results["segments"]:
            start = f"{int(segment['start'])//60}:{int(segment['start'])%60:02d}"
            if "speaker" in segment:
                f.write(f"[{start}] {segment['speaker'].title()}: {segment['text']}\n")
            else:
                f.write(f"[{start}] {segment['text']}\n")
        
        # Write statistics
        if "statistics" in results:
            f.write("\nConversation Statistics\n")
            f.write("="*30 + "\n")
            for speaker, stats in results["statistics"].items():
                f.write(f"\n{speaker.title()}:\n")
                f.write(f"- Total speaking time: {stats['total_time']:.1f}s\n")
                f.write(f"- Number of segments: {stats['segment_count']}\n")
                f.write(f"- Word count: {stats['word_count']}\n")

def _export_csv(results: Dict, output_path: Path):
    """Export results as CSV file."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Start", "End", "Speaker", "Text", "Confidence"])
        
        for segment in results["segments"]:
            writer.writerow([
                f"{int(segment['start'])//60}:{int(segment['start'])%60:02d}",
                f"{int(segment['end'])//60}:{int(segment['end'])%60:02d}",
                segment.get("speaker", ""),
                segment["text"],
                segment.get("confidence", "")
            ])

def _export_json(results: Dict, output_path: Path):
    """Export results as JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)