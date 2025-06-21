from processamento.vetorizacao import VectorStore


class EmbeddingService:
    def __init__(self):
        self.store = VectorStore()

    def add_text(self, text: str):
        self.store.add_texts([text])

    def query(self, text: str, k: int = 5):
        return self.store.query(text, k)
