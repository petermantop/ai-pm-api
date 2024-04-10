from django.urls import path
from .views import get_skills

urlpatterns = [
    path('', get_skills),
]
