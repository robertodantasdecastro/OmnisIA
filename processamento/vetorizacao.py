"""Vetorização de textos e armazenamento em FAISS."""
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class VectorStore:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []

    def add_texts(self, texts: List[str]):
        embeddings = self.model.encode(texts, show_progress_bar=False)
        self.index.add(np.array(embeddings, dtype="float32"))
        self.texts.extend(texts)

    def query(self, text: str, k: int = 5) -> List[str]:
        emb = self.model.encode([text])
        D, I = self.index.search(np.array(emb, dtype="float32"), k)
        return [self.texts[i] for i in I[0]]
