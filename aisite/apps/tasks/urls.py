from django.urls import path
from .views import create_task, go_chat, get_task

urlpatterns = [
    path("", create_task),
    path("<str:taskId>/", get_task),
    path("<str:taskId>/chat/", go_chat)
]
