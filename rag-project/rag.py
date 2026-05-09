import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

embedder = SentenceTransformer("all-MiniLM-L6-v2")

index = None
chunks = []


def load_documents(path: str, chunk_size: int = 500) -> list[str]:
    texts = []
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        for page in reader.pages:
            texts.append(page.extract_text() or "")
    else:
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())

    full_text = " ".join(texts)
    return [full_text[i : i + chunk_size] for i in range(0, len(full_text), chunk_size)]


def build_index(file_path: str):
    global index, chunks
    chunks = load_documents(file_path)
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))


def retrieve(query: str, top_k: int = 3) -> list[str]:
    if index is None or not chunks:
        return []
    query_vec = embedder.encode([query], convert_to_numpy=True).astype(np.float32)
    _, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]
