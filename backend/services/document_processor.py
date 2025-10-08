import os, re
from pypdf import PdfReader
import docx
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL = None

def _get_embedder():
    global MODEL
    if MODEL is None:
        print("INFO: Loading embedding model...")
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        print("INFO: Embedding model loaded.")
    return MODEL

class DocumentProcessor:
    def __init__(self):
        self.index = {}  # simple in-memory store: doc_id -> list of chunks

    # --- NEW METHOD ---
    def load_model(self):
        """Triggers the download and loading of the embedding model."""
        _get_embedder()

    def process_document(self, file_path: str):
        text = self.extract_text(file_path)
        chunks = self.dynamic_chunking(text, file_path)
        embedder = _get_embedder()
        embeddings = embedder.encode(chunks, show_progress_bar=False)
        doc_id = os.path.basename(file_path)
        self.index[doc_id] = [{'text': c, 'embedding': emb.tolist()} for c, emb in zip(chunks, embeddings)]
        return doc_id

    def extract_text(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.pdf':
            try:
                reader = PdfReader(file_path)
                pages = [p.extract_text() or '' for p in reader.pages]
                return '\n'.join(pages)
            except Exception:
                return ''
        elif ext in ('.docx', '.doc'):
            try:
                doc = docx.Document(file_path)
                return '\n'.join([p.text for p in doc.paragraphs])
            except Exception:
                return ''
        else:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception:
                return ''

    def dynamic_chunking(self, content: str, doc_type: str) -> list:
        if not content:
            return []
        words = content.split()
        chunk_size = 200
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks