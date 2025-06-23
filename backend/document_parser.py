# document_parser.py
from pdfminer.high_level import extract_text
import tempfile

def extract_text_from_file(uploaded_file):
    """
    Extracts text from uploaded PDF or TXT file.
    """
    if uploaded_file.name.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        return extract_text(tmp_path)

    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    else:
        return "Unsupported file format."

