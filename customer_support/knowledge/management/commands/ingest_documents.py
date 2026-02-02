from django.core.management.base import BaseCommand
from knowledge.models import Document, DocumentChunk, Embedding
from knowledge.utils import chunk_text
from knowledge.embedding_service import LocalEmbedder
from knowledge.vector_index import FAISSIndexManager
import numpy as np
import os

class Command(BaseCommand):
    help = "Ingest documents and create embeddings"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the document text file')
        parser.add_argument('--title', type=str, default='Untitled', help='Document title')
        parser.add_argument('--chunk_size', type=int, default=300, help='Chunk size in words')
        parser.add_argument('--overlap', type=int, default=50, help='Overlap size in words')

    def handle(self, *args, **options):
        file_path = options['file_path']
        title = options['title']
        chunk_size = options['chunk_size']
        overlap = options['overlap']

        if overlap >= chunk_size//2:
            self.stderr.write("Overlap must be less than half of chunk size.")
            return

        if not os.path.exists(file_path):
            self.stderr.write(f"File {file_path} does not exist.")
            return

        if Document.objects.filter(file_name=os.path.basename(file_path)).exists():
            self.stderr.write("Document already ingested.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        if not text.strip():
            self.stderr.write("File is empty.")
            return

        # Save Document
        doc = Document.objects.create(title=title, source_type='txt', file_name=os.path.basename(file_path))

        # Chunking
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        chunk_objs = []
        for idx, chunk in enumerate(chunks):
            chunk_objs.append(DocumentChunk(document=doc, chunk_index=idx, chunk_content=chunk))
        DocumentChunk.objects.bulk_create(chunk_objs)
        chunk_objs = list(DocumentChunk.objects.filter(document=doc))
        self.stdout.write(f"Created {len(chunk_objs)} chunks")

        # Embedding
        embedder = LocalEmbedder()
        embeddings = embedder.embed_texts([c.chunk_content for c in chunk_objs])
        self.stdout.write("Embeddings generated")

        # FAISS index
        index_manager = FAISSIndexManager()
        index_manager.add_vectors(embeddings)
        index_manager.save()
        self.stdout.write("FAISS index updated and saved")

        # Store vector IDs
        embedding_objs = []
        start_id = index_manager.index.ntotal - len(chunk_objs)
        for i, chunk_obj in enumerate(chunk_objs):
            vector_id = start_id + i
            embedding_objs.append(Embedding(document_chunk=chunk_obj, vector=vector_id))
        Embedding.objects.bulk_create(embedding_objs)

        self.stdout.write(self.style.SUCCESS(f"Ingested {len(chunks)} chunks for document '{title}'"))
