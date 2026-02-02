from django.urls import path
from knowledge.views import QueryAPIView

urlpatterns = [
    path('query/', QueryAPIView.as_view(), name='query'),
]
