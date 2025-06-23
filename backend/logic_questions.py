# logic_questions.py
import random
from transformers import pipeline

# Optional: Use a local LLM or OpenAI to generate better logical Qs
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")


def generate_logic_questions(doc_text):
    """
    Create 3 logic-based or comprehension questions from the text.
    """
    prompts = [
        "What is the main argument or conclusion presented?",
        "What assumptions does the text rely on?",
        "What are the implications of the main idea?",
        "Can you infer any challenges or limitations mentioned?",
        "What is the relationship between two key concepts in the text?"
    ]
    return random.sample(prompts, 3)


def evaluate_answers(questions, user_answers, context_text):
    """
    Evaluate user's answers by comparing to model-derived answer.
    Return (correct_flag, justification) for each.
    """
    results = []
    for question, user_ans in zip(questions, user_answers):
        try:
            result = qa_pipeline(question=question, context=context_text)
            model_ans = result['answer'].strip().lower()
            user_ans_clean = user_ans.strip().lower()
            correct = model_ans in user_ans_clean or user_ans_clean in model_ans
            snippet = context_text[result['start']:result['end']+120]
        except:
            correct = False
            snippet = "Could not evaluate."

        justification = f"Expected answer was: '{model_ans}'. Found in: \"{snippet.strip()}\""
        results.append((correct, justification))

    return results
