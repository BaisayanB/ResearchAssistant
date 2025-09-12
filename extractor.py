# extractor.py
import re
import os
import fitz
import arxiv
import requests
import tempfile

def fetch_arxiv_metadata(arxiv_id: str) -> dict:
    search = arxiv.Search(id_list=[arxiv_id])
    result = next(search.results())
    metadata = {
        "arxiv_id": arxiv_id, "title": result.title, "authors": [a.name for a in result.authors],
        "published": result.published.strftime("%Y-%m-%d"), "updated": result.updated.strftime("%Y-%m-%d"),
        "categories": result.categories, "url": result.entry_id
    }
    return {k: v for k, v in metadata.items() if v is not None}

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    parts = []
    for page in doc:
        txt = page.get_text("text") or ""
        txt = txt.replace("-\n", "")
        txt = txt.replace("\n", " ")
        parts.append(txt.strip())
    full = " ".join(parts)
    full = re.sub(r"\s+", " ", full)
    full = re.sub(r"\[\s*\d+(?:[\-,]\s*\d+)*(?:\s*,\s*\d+(?:[\-,]\d+)*)*\s*\]", "", full)
    full = re.sub(r"\s{2,}", " ", full)
    return full.strip()

def slice_abstract_to_references(text: str) -> str:
    lower = text.lower()    
    start = lower.find("abstract")
    if start == -1: start = 0
    end = lower.find("references")
    if end == -1: end = len(text)
    sliced = text[start:end].strip()
    return re.sub(r"\s+", " ", sliced)

# --- MODIFICATION: This function now accepts the correct arxiv_id ---
def extract_with_metadata(pdf_path: str, arxiv_id: str) -> dict:
    """Main pipeline: arxiv metadata + sliced text."""
    # --- FIX: We REMOVED the line that guessed the ID from the filename ---
    metadata = fetch_arxiv_metadata(arxiv_id)
    raw_text = extract_text(pdf_path)
    content = slice_abstract_to_references(raw_text)
    return {"metadata": metadata, "content": content}

# --- MODIFICATION: This function now also accepts and passes the arxiv_id ---
def process_pdf_from_url(pdf_url: str, arxiv_id: str) -> dict:
    """
    Downloads a PDF from a URL, saves it temporarily, and then runs your
    existing `extract_with_metadata` function on it.
    """
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(response.content)
            temp_filepath = temp_file.name
        
        # --- FIX: Pass the correct arxiv_id to the next function ---
        result = extract_with_metadata(temp_filepath, arxiv_id)
        
    finally:
        if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
            os.unlink(temp_filepath)
            
    return result