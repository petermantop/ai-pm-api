from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..user.models import Requester, Tasker
from bson import ObjectId
import json


@api_view(["GET"])
def get_profile(request, id):

    requester = Requester.objects(id=id).first()
    tasker = Tasker.objects(id=id).first()
    user = requester or tasker

    print(user.id)
    if user is None:
        return JsonResponse({"message": "Invalid request, User not found"}, status=400)

    user_dict = user.to_mongo().to_dict()
    for key, value in user_dict.items():
        if isinstance(value, ObjectId):
            user_dict[key] = str(value)

    return Response(user_dict, status=200)


# Create your views here.
@api_view(["POST"])
def update_profile(request):
    # get user id here(will be changed accordingly) from session
    userId = request.session["userId"]

    requester = Requester.objects(id=userId).first()
    tasker = Tasker.objects(id=userId).first()

    user = requester or tasker

    if user is None:
        return JsonResponse({"message": "Invalid request, User not found"}, status=400)

    for key, value in request.data.items():
        # Skip 'userId' key as it's not a field of Tasker
        if key != "userId" and key != "role":
            setattr(user, key, value)

    # Save the updated user object
    user.save()
    user_dict = user.to_mongo().to_dict()
    for key, value in user_dict.items():
        if isinstance(value, ObjectId):
            user_dict[key] = str(value)

    return Response(user_dict, status=200)
