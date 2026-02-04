from django.urls import path
from knowledge.views import QueryAPIView, DashboardView, DocumentUploadView, SubmissionsView

urlpatterns = [
    path('query/', QueryAPIView.as_view(), name='query'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('upload/', DocumentUploadView.as_view(), name='document_upload'),
    path('submissions/', SubmissionsView.as_view(), name='submissions'),
]
