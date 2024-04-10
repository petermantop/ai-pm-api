from django.urls import path
from .views import create_task

urlpatterns = [
    path('', create_task)
]
