from django.urls import path
from ingestion.views import APIIngestView

urlpatterns = [
    path('', APIIngestView.as_view(), name='ingest'),
]
