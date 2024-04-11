import openai
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, SubTask
from .serializers import TaskSerializer
from django.conf import settings
import os

import json

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": message} for message in messages],
    )
    return response


# @api_view(['POST'])
# def create_task(request):
#     # get user id here(will be changed accordingly)
#     userId  = request.data.get("id")

#     messages = request.data.get('messages')
#     result = get_openai_response(messages)
#     return Response(result, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_task(request):
    data = json.loads(request.body)
    title = data.get("title")
    description = data.get("description")
    requester = data.get("requester")
    status = "open"
    print(title, description, requester, status)
    task = Task(
        title=title, description=description, requester=requester, status=status
    )
    task.save()

    subtask = SubTask(
        title="Subtask title",
        description="Subtask Description",
        status="open",  # Set the initial status of the subtask
    )
    task.tasks.append(subtask)
    task.save()

    print(task.tasks[0]._id)

    return Response("Task Created Successfully", status=201)
