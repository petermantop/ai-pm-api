from django.urls import path
from .views import get_agents

urlpatterns = [
    path('', get_agents),
]
