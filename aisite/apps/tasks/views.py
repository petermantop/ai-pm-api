import openai
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.conf import settings
import os

import json

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message}
            for message in messages
        ],
    )
    return response

# @api_view(['POST'])
# def create_task(request):
#     # get user id here(will be changed accordingly)
#     userId  = request.data.get("id")

#     messages = request.data.get('messages')
#     result = get_openai_response(messages)
#     return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_task(request):
    data = json.loads(request.body)
    name = data.get("name")
    description = data.get("description")
    requester = data.get('requester')
    subtasks = data.get("subtasks", [])
    status = 'open'
    print(name, description, requester, subtasks, status)
    task = Task.objects.create(
        name=name,
        description=description,
        requester=requester,
        subtasks=subtasks,
        status=status
    )
    
    return Response("Task Created Successfully", status=201)