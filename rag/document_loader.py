# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parents[1]
# DOCUMENTS_DIR = BASE_DIR / "documents"

# def load_documents():
#     documents = []

#     for file_path in DOCUMENTS_DIR.glob("*.txt"):
#         documents.append({
#             "file_name": file_path.name,
#             "content": file_path.read_text(encoding="utf-8")
#         })

#     return documents



from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = BASE_DIR / "documents"


def load_text_file(file_path):
    return file_path.read_text(encoding="utf-8")


def load_pdf_file(file_path):

    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def load_documents():

    documents = []

    # Load TXT files
    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        documents.append({
            "file_name": file_path.name,
            "content": load_text_file(file_path)
        })

    # Load PDF files
    for file_path in DOCUMENTS_DIR.glob("*.pdf"):

        documents.append({
            "file_name": file_path.name,
            "content": load_pdf_file(file_path)
        })

    return documents