from typing import List
import os

def load_text_file(filepath: str) -> str:
    """Reads a text file and returns the content as a string."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_list_from_file(filepath: str) -> List[str]:
    """Reads a text file (one item per line) and returns a list of strings."""
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace, and ignore empty lines
        return [line.strip() for line in f.readlines() if line.strip()]