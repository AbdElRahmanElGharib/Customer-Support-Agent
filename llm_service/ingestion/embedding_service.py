from sentence_transformers import SentenceTransformer
import numpy as np

class LocalEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        """
        Args:
            texts (list[str]): list of strings
        Returns:
            np.ndarray: embeddings of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])
        return self.model.encode(texts, convert_to_numpy=True)
