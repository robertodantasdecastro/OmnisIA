import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from ..config import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """Inicializa o serviço de embeddings"""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def add_texts(self, texts: List[str]):
        """Adiciona textos ao índice vetorial"""
        try:
            # Gera embeddings
            embeddings = self.model.encode(texts)

            # Inicializa o índice FAISS se necessário
            if self.index is None:
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)

            # Adiciona ao índice
            self.index.add(embeddings.astype("float32"))
            self.texts.extend(texts)

        except Exception as e:
            raise Exception(f"Erro ao adicionar textos: {str(e)}")

    def query(self, text: str, k: int = 5) -> List[Tuple[str, float]]:
        """Consulta textos similares"""
        try:
            if self.index is None or len(self.texts) == 0:
                return []

            # Gera embedding da query
            query_embedding = self.model.encode([text])

            # Busca no índice
            distances, indices = self.index.search(query_embedding.astype("float32"), k)

            # Retorna resultados
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.texts):
                    results.append((self.texts[idx], float(distance)))

            return results

        except Exception as e:
            raise Exception(f"Erro na consulta: {str(e)}")

    def add_text(self, text: str):
        """Adiciona um único texto"""
        self.add_texts([text])
