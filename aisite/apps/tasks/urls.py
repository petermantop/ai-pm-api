from django.urls import path
from .views import create_task, get_task

urlpatterns = [
    path('', create_task),
    path('api/tasks/<int:pk>', get_task),
]
