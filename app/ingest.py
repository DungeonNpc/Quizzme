from pypdf import PdfReader
from dataclasses import dataclass

MIN_CHARS = 100

@dataclass
class Chunk:
    text: str
    page: int



def clean(text):
    cleaned_text = " ".join(text.split())
    return cleaned_text

def extract_pages(pdf_path):
    reader = PdfReader(pdf_path)
    pages_text = []
    for pagenum, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages_text.append((pagenum, clean(text)))
    return pages_text

def split_text(text, max_chars: int = 3000):
    chunks = []
    while len(text) > max_chars:
        cut = text.rfind(' ', 0, max_chars + 1)
        if cut == -1:
            cut = max_chars
        chunks.append(text[:cut].strip())
        text = text[cut:].strip()
    if text.strip():
        chunks.append(text.strip())
    return chunks

def chunk_pages(pages, max_chars: int = 3000):
    chunks = []
    for page_num, text in pages:
        for piece in split_text(text, max_chars):
            if len(piece) >= MIN_CHARS:   
                chunks.append(Chunk(text = piece, page = page_num))
    return chunks

if __name__ == "__main__":
    pages = extract_pages("eval/docs/Linux cheatsheet.pdf")
    chunks = chunk_pages(pages, 500)
    print(len(chunks))
    print([c.text for c in chunks])