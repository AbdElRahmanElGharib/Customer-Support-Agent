from django.urls import path
from main.views import HomeView, APIMessageView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/', APIMessageView.as_view(), name='api'),
]
