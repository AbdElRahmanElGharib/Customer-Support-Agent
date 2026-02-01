from django.contrib import admin
from .models import Document, DocumentChunk, Embedding

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentChunk)
admin.site.register(Embedding)
