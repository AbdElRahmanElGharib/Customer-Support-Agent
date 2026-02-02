from django.urls import path
from knowledge.views import QueryAPIView, DashboardView

urlpatterns = [
    path('query/', QueryAPIView.as_view(), name='query'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
