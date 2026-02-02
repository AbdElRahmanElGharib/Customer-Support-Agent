from knowledge.embedding_service import LocalEmbedder
from knowledge.vector_index import FAISSIndexManager
from knowledge.models import Embedding
from knowledge.llm_service import LocalLLMService
import time

class RAGQueryService:
    def __init__(self, top_k=5, index_path='faiss.index', embedding_dim=384):
        self.top_k = top_k
        self.embedder = LocalEmbedder()
        self.index_manager = FAISSIndexManager(index_path=index_path)
        self.embedding_dim = embedding_dim
        self.llm = LocalLLMService()

    def query(self, question):
        """
        Args:
            question (str): user question
        Returns:
            list[str]: top_k most relevant chunks (content)
        """
        if not question.strip():
            return []

        # Step 1: compute embedding
        question_vec = self.embedder.embed_texts([question])

        if question_vec.size == 0:
            return []

        # Step 2: search FAISS
        _, indices = self.index_manager.index.search(question_vec, self.top_k) # pyright: ignore[reportCallIssue]

        # Step 3: map FAISS indices to chunks
        chunks = []
        for idx in indices[0]:
            if idx < 0:
                continue
            try:
                embedding_obj = Embedding.objects.get(vector=idx)
                chunks.append(embedding_obj.document_chunk.chunk_content)
            except Embedding.DoesNotExist:
                continue

        return chunks

    def query_with_llm(self, question, top_k=5):
        chunks = self.query(question)
        if not chunks:
            return ""
        print(f"Retrieved {len(chunks)} chunks for the question.\n Now generating answer...")
        start_time = time.time()
        output = self.llm.generate_answer(question, chunks)
        print(f"Answer generated in {time.time() - start_time:.2f} seconds.")
        return output
