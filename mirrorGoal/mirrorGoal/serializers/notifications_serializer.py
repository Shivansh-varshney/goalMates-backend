from rest_framework import serializers
from mirrorGoal.models import Notifications

class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['id', 'user', 'type', 'data', 'is_read', 'created_at']