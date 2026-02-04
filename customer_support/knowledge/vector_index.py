import faiss
import numpy as np
import os

class FAISSIndexManager:
    def __init__(self, embedding_dim=384, index_path='faiss.index'):
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(embedding_dim)

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

    def add_vectors(self, vectors: np.ndarray):
        """vectors: np.ndarray, shape=(n, embedding_dim)"""
        if vectors.size == 0:
            return
        vectors = vectors.astype('float32')
        if vectors.ndim != 2 or vectors.shape[1] != self.embedding_dim:
            raise ValueError(
                f"Expected shape (n, {self.embedding_dim}), got {vectors.shape}"
            )
        self.index.add(vectors) # type: ignore

    def save(self):
        faiss.write_index(self.index, self.index_path)

    def clear(self):
        self.index.reset()
        faiss.write_index(self.index, self.index_path)
