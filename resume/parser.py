import pdfplumber
from docx import Document
import os

def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def parse_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(file_path):
    if not os.path.exists(file_path):
        print(f"❌  File not found: {file_path}")
        return None

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        print("📄  Parsing PDF resume...")
        return parse_pdf(file_path)
    elif ext == ".docx":
        print("📄  Parsing DOCX resume...")
        return parse_docx(file_path)
    else:
        print("❌  Unsupported file type. Use PDF or DOCX.")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python resume/parser.py <path_to_resume>")
    else:
        text = parse_resume(sys.argv[1])
        if text:
            print("\n--- EXTRACTED TEXT ---\n")
            print(text[:1000])
            print("\n... (truncated)")
