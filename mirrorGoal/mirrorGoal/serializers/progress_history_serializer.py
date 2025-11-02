from rest_framework import serializers
from mirrorGoal.models import ProgressHistory, Goal

class ProgressHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProgressHistory
        fields = ['id', 'recorded_at', 'progress']

class Serializer(serializers.ModelSerializer):
    history = ProgressHistorySerializer(
        many=True, 
        read_only=True
    )

    class Meta:
        model  = Goal
        fields = ['id', 'title', 'history']