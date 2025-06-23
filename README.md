# README.md

# 📄 Smart Assistant for Research Summarization

An AI-powered research tool that allows users to upload documents (PDF or TXT), automatically summarizes them, answers questions based on their content, and generates logic-based challenges to test comprehension.

---

## 🚀 Features

- 📤 Upload structured documents (PDF or TXT)
- 📌 Get concise summaries (≤ 150 words)
- ❓ Ask Anything mode with contextual answers + justification
- 🧠 Challenge Me mode with 3 logic/comprehension questions
- 📎 All answers cite the supporting document snippet

---

## 🧑‍💻 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-assistant-genai.git
cd smart-assistant-genai
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv assistant_env
source assistant_env/bin/activate  # Windows: assistant_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser to use the app.

---

## 📂 Project Structure
```
smart-assistant/
├── app.py                   # Main Streamlit app
├── backend/
│   ├── document_parser.py   # Extracts text from PDFs/TXTs
│   ├── summarizer.py        # Summarizes the text
│   ├── qa_engine.py         # Answers user questions
│   ├── logic_questions.py   # Generates and evaluates logic Qs
│   └── utils.py             # Common utilities (chunking, cleaning)
├── requirements.txt
└── README.md
```

---

## 💡 Notes

- All responses are derived strictly from uploaded content.
- QA uses chunked matching with `DistilBERT` for better contextual alignment.
- Optional: connect OpenAI API for advanced question generation.

---

## 📸 Optional Demo
You can record a demo using [Loom](https://loom.com) or upload a YouTube video walkthrough and link it in the repo.

---

## 📜 License
MIT License – use freely for learning and academic purposes.
