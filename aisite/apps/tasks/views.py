from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, SubTask, Chat
from .serializers import TaskSerializer
from django.conf import settings
import os
import json
import requests
from .forms import ChatForm


@api_view(["POST"])
def create_task(request):
    userId = "661918fdd7d5867033aebcec"  # request.session["userId"]
    task = Task(requester=userId).save()

    return Response({"taskId": str(task.id)}, status=201)


@api_view(["POST"])
def go_chat(request, taskId):
    task = Task.objects.filter(id=taskId).first()
    data = json.loads(request.body)
    form = ChatForm(data)
    if task is None:
        return Response({"message": "Task Not Found"}, safe=False, status=400)

    if form.is_valid():
        message = data.get("message")
        history = data.get("history")

        # get ai reponse from openai-server
        response = requests.post(
            os.getenv("OPENAI_CHAT_SERVER_URL"),
            json={"message": message, "history": history},
        )
        response = response.json()
        print(response, response["response"])
        # add chat
        chat = Chat(
            message=message, response=response["response"], history=response["history"]
        )
        task.chat.append(chat)
        task.save()

        # create sub tasks
        if response["is_final_outline"] is True:
            for sub_task in response["final_outline"]["main_tasks"][0]["sub_tasks"]:
                subTask = SubTask(
                    title=sub_task["title"],
                    description=sub_task["descriptions"],
                    worker=sub_task["worker"],
                    cost=sub_task["cost"],
                )
                task.tasks.append(subTask)
            task.save()

        print("message, history", response)
        return Response(response, status=200)
    else:
        return Response(
            {"message": "Invalid inputs", "errors": form.errors}, safe=False, status=400
        )
