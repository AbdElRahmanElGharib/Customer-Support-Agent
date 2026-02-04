from django.contrib import admin
from .models import Document, DocumentChunk, Embedding, DocumentSubmission

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentChunk)
admin.site.register(Embedding)

@admin.register(DocumentSubmission)
class DocumentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'last_updated')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'last_updated')
