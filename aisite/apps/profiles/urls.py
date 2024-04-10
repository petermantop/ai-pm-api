from django.urls import path
from .views import update_profile, get_profile

urlpatterns = [
    path('', update_profile),
    path('<str:id>', get_profile)
]
