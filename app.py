
import streamlit as st
from backend.document_parser import extract_text
from backend.summarizer import generate_summary
from backend.qa_engine import answer_question
from backend.logic_questions import generate_logic_questions, evaluate_answers

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📄 Smart Assistant for Document Summarization")

# Initialize session state
if 'doc_text' not in st.session_state:
    st.session_state.doc_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'challenge_questions' not in st.session_state:
    st.session_state.challenge_questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'results' not in st.session_state:
    st.session_state.results = None
if 'questions_generated' not in st.session_state:  # NEW FLAG
    st.session_state.questions_generated = False

# File uploader
uploaded_file = st.file_uploader("Upload your research document (PDF or TXT):", type=["pdf", "txt"])
if uploaded_file:
    st.session_state.doc_text = extract_text(uploaded_file)
    st.session_state.summary = generate_summary(st.session_state.doc_text)
    st.subheader("📌 Document Summary")
    st.write(st.session_state.summary)

    # Reset challenge state when new document is uploaded
    st.session_state.challenge_questions = []
    st.session_state.user_answers = []
    st.session_state.results = None
    st.session_state.questions_generated = False  # Reset flag on new upload

# Mode selection
if st.session_state.doc_text:
    mode = st.radio("Choose a mode:", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        query = st.text_input("Ask a question about the document:")
        if query:
            response, justification = answer_question(query, st.session_state.doc_text)
            st.markdown(f"**Answer:** {response}")
            st.markdown(f"_Justification:_ {justification}")

    elif mode == "Challenge Me":
        # Only generate questions once
        if not st.session_state.questions_generated:
            with st.spinner("Generating comprehension questions..."):
                st.session_state.challenge_questions = generate_logic_questions(st.session_state.doc_text)
                st.session_state.user_answers = [""] * len(st.session_state.challenge_questions)
                st.session_state.results = None
                st.session_state.questions_generated = True
                st.session_state.submitted = False  # NEW: add submitted flag

        if st.session_state.challenge_questions:
            st.subheader("🧠 Challenge Yourself!")
            st.write("Answer the following questions:")

            # Display questions and collect answers (safe assignment)
            for i, q in enumerate(st.session_state.challenge_questions):
                answer = st.text_input(
                    f"Q{i + 1}: {q}",
                    value=st.session_state.user_answers[i],
                    key=f"q{i}"
                )
                st.session_state.user_answers[i] = answer

            # Submit Button
            if st.button("✅ Submit Answers"):
                if any(ans.strip() == "" for ans in st.session_state.user_answers):
                    st.error("Please answer all questions before submitting.")
                    st.session_state.submitted = False
                else:
                    with st.spinner("Evaluating answers..."):
                        st.session_state.results = evaluate_answers(
                            st.session_state.challenge_questions,
                            st.session_state.user_answers,
                            st.session_state.doc_text
                    )
                    st.session_state.submitted = True  # only show results after submission

        # Show results **only after submit is clicked**
        if st.session_state.get('submitted') and st.session_state.results:
            for i, result in enumerate(st.session_state.results):
                st.markdown(f"### Q{i + 1} Feedback")
                st.markdown(f"**Question:** {result['question']}")
                st.markdown(f"**Your Answer:** {result['user_answer']}")
                st.markdown(f"**Model Answer:** {result['model_answer']}")
                st.markdown(f"**Answer Status:** {'✅ Correct' if result['is_correct'] else '❌ Incorrect'}")
                st.markdown(f"**Justification:** {result['justification']}")

