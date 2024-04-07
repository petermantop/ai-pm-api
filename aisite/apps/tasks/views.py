import openai
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.conf import settings
import os

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

@api_view(['POST'])
def create_task(request):
    # get user id here(will be changed accordingly)
    userId  = request.data.get("id")

    messages = request.data.get('messages')
    result = get_openai_response(messages)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task)
    return Response(serializer.data)
