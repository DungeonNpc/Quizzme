from pypdf import PdfReader
from dataclasses import dataclass

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
            chunks.append(Chunk(text = piece, page = page_num))
    return chunks

if __name__ == "__main__":
    fake_pages = [(1, "one two three four five six"), (2, "seven eight nine")]
    for c in chunk_pages(fake_pages, 10):
        print(c.page, c.text)