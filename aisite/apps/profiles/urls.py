from django.urls import path
from .views import update_profile

urlpatterns = [
    path('', update_profile),
]
