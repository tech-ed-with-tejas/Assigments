from io import BytesIO
from pypdf import PdfReader

def read_pdf_pages_from_bytes(pdf_bytes: bytes) -> list[str]:
    """Reads PDF content from bytes and returns a list of text per page."""
    reader = PdfReader(BytesIO(pdf_bytes))
    output = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        # Optional simple normalization
        txt = "\n".join(line.strip() for line in txt.splitlines())
        output.append(txt)
    return output




if __name__ == "__main__":
    with open("./sampledata/3.pdf", "rb") as f:
        pdf_bytes = f.read()
    pages = read_pdf_pages_from_bytes(pdf_bytes)
    for idx, content in enumerate(pages, start=1):
        print(f"--- Page {idx} ---\n{content}\n")