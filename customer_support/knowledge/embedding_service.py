import numpy as np
import requests
from django.conf import settings

class EmbeddingServiceError(Exception):
    pass

class LocalEmbedder:
    def embed_texts(self, texts):
        """
        Args:
            texts (list[str]): list of strings
        Returns:
            np.ndarray: embeddings of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])
        
        url = f'{settings.LLM_SERVICE_BASE_URL}/embed/'
        payload = {'text': texts}

        try:
            response = requests.post(url, json=payload, timeout=30)
        except requests.RequestException as exc:
            raise EmbeddingServiceError('Failed to reach embedding service') from exc

        if response.status_code != 200:
            raise EmbeddingServiceError(
                f'Embedding service error: {response.status_code} - {response.text}'
            )

        data = response.json()
        return np.array(data['embedding'])
