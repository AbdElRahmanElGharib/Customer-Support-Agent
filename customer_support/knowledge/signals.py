from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings

from .models import DocumentSubmission

@receiver(post_save, sender=DocumentSubmission)
@receiver(post_delete, sender=DocumentSubmission)
def invalidate_document_submission_cache(sender, **kwargs):
    cache.delete(settings.SUBMISSIONS_CACHE_KEY)
