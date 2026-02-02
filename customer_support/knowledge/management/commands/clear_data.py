from django.core.management.base import BaseCommand
from knowledge.vector_index import FAISSIndexManager
from knowledge.models import Document, DocumentChunk, Embedding

class Command(BaseCommand):
    help = "Clear the FAISS vector index"

    def handle(self, *args, **options):
        index_manager = FAISSIndexManager()
        index_manager.clear()
        self.stdout.write(self.style.SUCCESS("FAISS index cleared successfully"))
        Document.objects.all().delete()
        DocumentChunk.objects.all().delete()
        Embedding.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All documents, chunks, and embeddings deleted successfully"))
