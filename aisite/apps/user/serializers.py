from rest_framework import serializers
from .models import Tasker, Requester

class TaskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasker
        fields = '__all__'


class RequesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requester
        fields = '__all__'
