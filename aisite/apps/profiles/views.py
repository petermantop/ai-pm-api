from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..user.models import Requester, Tasker
from bson import ObjectId

# Create your views here.
@api_view(['POST'])
def update_profile(request):
    # get user id here(will be changed accordingly) from session
    userId  = ObjectId(request.data.get("userId"))
    role  = request.data.get("role")

    if role == 'requester':
        user = Requester.objects(id=userId).first()
    else:
        user = Tasker.objects(id=userId).first()

    if user is None:
        return JsonResponse(
            {"message": "Invalid request, User not found"},
            status=400
        )
    
    for key, value in request.data.items():
        # Skip 'userId' key as it's not a field of Tasker
        if key != "userId" and key != "role":
            setattr(user, key, value)
    
    # Save the updated user object
    user.save()
    return Response(str(userId), status=200)