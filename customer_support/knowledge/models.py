from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
