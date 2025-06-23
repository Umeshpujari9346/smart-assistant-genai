# summarizer.py
from transformers import pipeline
import re

# Load pre-trained summarizer (can use T5, BART, etc.)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    """
    Generates a summary of ≤150 words from the given document text.
    """
    # Clean up long newlines and excessive spacing
    text = re.sub(r"\s+", " ", text.strip())
    # Limit to first 1024 tokens for performance
    text = text[:3000]  # Adjust token cut based on model size
    summary = summarizer(text, max_length=150, min_length=60, do_sample=False)
    return summary[0]['summary_text']
