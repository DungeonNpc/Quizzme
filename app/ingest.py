from pypdf import PdfReader
from dataclasses import dataclass
from pathlib import Path

MIN_CHARS = 100
MIN_TOTAL_CHARS = 200

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

def ingest(path):
    suffix = Path(path).suffix.lower()
    if suffix == '.pdf':
        pages = extract_pages(path)
    elif suffix == '.txt':
        pages = [(1,clean(Path(path).read_text(encoding="utf-8")))]
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    total = sum(len(text) for _, text in pages)
    if total < MIN_TOTAL_CHARS:
        raise ValueError("No readable text found. The file may be a scanned PDF.")
    chunks = chunk_pages(pages)
    if not chunks:
        raise ValueError(f"No chunk reached {MIN_CHARS} characters. The document may be too fragmented.")
    return chunks

if __name__ == "__main__":
    # split_text
    print(split_text("one two three four five six", 10))
    print(split_text("short", 10))
    print(split_text("", 10))
    print(split_text("abcdefghijklmnopqrstuvwxyz", 10))
    print(split_text("abcdefghij", 10))

    # chunk_pages (MIN_CHARS filter)
    fake_pages = [(1, "a" * 150), (2, "short text")]
    print([(c.page, len(c.text)) for c in chunk_pages(fake_pages, 200)])

    # ingest: pdf
    try:
        chunks = ingest("eval/docs/Linux cheatsheet.pdf")
        print(len(chunks), [c.page for c in chunks])
    except Exception as e:
        print("pdf FAILED:", e)

    # ingest: txt
    try:
        print("test.txt length:", len(Path("eval/docs/test.txt").read_text(encoding="utf-8")))
        chunks = ingest("eval/docs/test.txt")
        print(len(chunks), chunks[0])
    except Exception as e:
        print("txt FAILED:", e)

    # ingest: unsupported type
    try:
        ingest("eval/docs/fake.docx")
        print("docx FAILED: no error was raised")
    except ValueError as e:
        print("caught:", e)

    # ingest: empty file
    try:
        ingest("eval/docs/empty.txt")
        print("empty FAILED: no error was raised")
    except ValueError as e:
        print("caught:", e)