from django.urls import path
from .views import get_daos

urlpatterns = [
    path('', get_daos),
]
