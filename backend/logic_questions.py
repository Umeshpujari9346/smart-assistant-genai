


import streamlit as st
import re
from transformers import pipeline
from backend.qa_engine import answer_question
from backend.summarizer import generate_summary
import logging

qg_pipeline = pipeline("text-generation", model="gpt2")

@st.cache_data
def generate_logic_questions(document_text, num_questions=3):
    """Generate comprehension questions using GPT-2 with simplified approach"""

    clean_text = re.sub(r"\s+", " ", document_text.strip())
    context = clean_text[:500]  # Use only first 500 characters
    print("context:",context)

    if not context:
        return ["Document text is empty or invalid."]


    prompt = (
        f"Create {num_questions} short questions about this text: '{context}'\n\n"
        f"Questions:\n1. "
    )

    try:

        response = qg_pipeline(
            prompt,
            max_new_tokens=100,
            num_return_sequences=1,
            truncation=True,
            do_sample=True,
            temperature=0.5,
            top_k=50,
            no_repeat_ngram_size=3
        )

        generated_text = response[0]['generated_text']
        print(f"Generated text: {generated_text}")


        generated_part = generated_text.split("Questions:\n")[-1].strip()


        question_lines = []
        for line in generated_part.split('\n'):
            line = line.strip()

            if re.match(r'^\d+\.', line):
                line = re.sub(r'^\d+\.\s*', '', line)
            question_lines.append(line)


        questions = []
        for q in question_lines[:num_questions]:
            print('q',q)
            q = q.strip()

            q = q.replace('"', '').replace("'", '')

            if q and not q.endswith('?'):
                q += '?'
            questions.append(q)

        return questions if questions else ["What is the main topic?"]

    except Exception as e:
        print(f"Question generation error: {e}")

        return [
            "What is the main topic of this document?",
            "What problem does this text address?",
            "What solution is proposed?"
        ]


@st.cache_data
def evaluate_answers(questions, user_answers, document_text):

    results = []

    for question, user_answer in zip(questions, user_answers):


        model_answer, justification = answer_question(question, document_text)


        clean_user = user_answer.lower().strip()
        clean_model = model_answer.lower().strip()


        is_correct = (
                clean_model in clean_user or
                clean_user in clean_model or
                any(word in clean_user for word in clean_model.split() if len(word) > 4)
        )

        results.append({
            "question": question,
            "user_answer": user_answer,
            "model_answer": model_answer,
            "is_correct": is_correct,
            "justification": justification
        })

    return results


