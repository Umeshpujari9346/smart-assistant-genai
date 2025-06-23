# qa_engine.py
from transformers import pipeline
from backend.utils import chunk_text

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def answer_question(question, context_text):
    """
    Returns the best-matching answer and the document snippet it came from.
    """
    chunks = chunk_text(context_text, chunk_size=500)
    results = []

    for chunk in chunks:
        try:
            result = qa_pipeline(question=question, context=chunk)
            result['context'] = chunk[:300] + "..."
            results.append(result)
        except:
            continue

    if not results:
        return "Sorry, I couldn't find an answer.", "No context available."

    # Sort by score and return best answer
    best = sorted(results, key=lambda x: x['score'], reverse=True)[0]
    return best['answer'], f"Supported by: \"{best['context']}\""
