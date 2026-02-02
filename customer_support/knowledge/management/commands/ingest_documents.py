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

    def handle(self, *args, **options):
        file_path = options['file_path']
        title = options['title']

        if not os.path.exists(file_path):
            self.stderr.write(f"File {file_path} does not exist.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Save Document
        doc = Document.objects.create(title=title, source_type='txt', original_filename=os.path.basename(file_path))

        # Chunking
        chunks = chunk_text(text)
        chunk_objs = []
        for idx, chunk in enumerate(chunks):
            chunk_objs.append(DocumentChunk(document=doc, chunk_index=idx, content=chunk))
        DocumentChunk.objects.bulk_create(chunk_objs)

        # Embedding
        embedder = LocalEmbedder()
        embeddings = embedder.embed_texts([c.content for c in chunk_objs])

        # FAISS index
        index_manager = FAISSIndexManager()
        index_manager.add_vectors(embeddings)
        index_manager.save()

        # Store vector IDs
        for chunk_obj, vector_id in zip(chunk_objs, range(index_manager.index.ntotal - len(chunk_objs), index_manager.index.ntotal)):
            Embedding.objects.create(chunk=chunk_obj, vector_id=vector_id)

        self.stdout.write(self.style.SUCCESS(f"Ingested {len(chunks)} chunks for document '{title}'"))
