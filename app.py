# app.py
import streamlit as st
from backend.document_parser import extract_text
from backend.summarizer import generate_summary
from backend.qa_engine import answer_question
from backend.logic_questions import generate_logic_questions, evaluate_answers

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📄 Smart Assistant for Research Summarization")

# Session State
if 'doc_text' not in st.session_state:
    st.session_state.doc_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""

# Upload File
uploaded_file = st.file_uploader("Upload your research document (PDF or TXT):", type=["pdf", "txt"])
if uploaded_file:
    st.session_state.doc_text = extract_text(uploaded_file)
    st.session_state.summary = generate_summary(st.session_state.doc_text)
    st.subheader("📌 Document Summary")
    st.write(st.session_state.summary)

    # Mode Selection
    mode = st.radio("Choose a mode:", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        query = st.text_input("Ask a question about the document:")
        if query:
            response, justification = answer_question(query, st.session_state.doc_text)
            st.markdown(f"**Answer:** {response}")
            st.markdown(f"_Justification:_ {justification}")

    elif mode == "Challenge Me":
        questions = generate_logic_questions(st.session_state.doc_text)
        user_answers = []
        st.write("Answer the following questions:")
        for i, q in enumerate(questions):
            user_input = st.text_input(f"Q{i+1}: {q}", key=f"q{i}")
            user_answers.append(user_input)

        if st.button("Submit Answers"):
            results = evaluate_answers(questions, user_answers, st.session_state.doc_text)
            for i, (correct, justification) in enumerate(results):
                st.markdown(f"**Q{i+1} Feedback:** {'✅ Correct' if correct else '❌ Incorrect'}")
                st.markdown(f"_Justification:_ {justification}")
