# utils.py

import re

def clean_text(text):
    """Remove extra whitespace and normalize text."""
    return re.sub(r"\s+", " ", text.strip())

def chunk_text(text, chunk_size=500):
    """Split text into word-based chunks."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def count_words(text):
    return len(text.split())

