from celery import shared_task
from .models import DocumentSubmission
from knowledge.management.commands.ingest_documents import Command as IngestCommand

@shared_task(bind=True, name="process_document")
def process_document(self, submission_id: int):
    submission = DocumentSubmission.objects.get(pk=submission_id)

    try:
        submission.status = DocumentSubmission.Status.IN_PROGRESS
        submission.save(update_fields=["status"])

        IngestCommand().handle(
            file_path=submission.file.path,
            title=submission.file.name,
            chunk_size=300,
            overlap=50
        )

        submission.status = DocumentSubmission.Status.SUCCEEDED
        submission.save(update_fields=["status"])

    except Exception:
        submission.status = DocumentSubmission.Status.FAILED
        submission.save(update_fields=["status"])
        raise
