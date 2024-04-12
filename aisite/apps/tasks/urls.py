from django.urls import path
from .views import create_task, go_chat

urlpatterns = [path("", create_task), path("<str:taskId>/chat/", go_chat)]
