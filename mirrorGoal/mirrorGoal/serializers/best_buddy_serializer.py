from rest_framework import serializers
from mirrorGoal.models import User, Partnership, Goal

class Serializer(serializers.Serializer):

    username = serializers.CharField()
    