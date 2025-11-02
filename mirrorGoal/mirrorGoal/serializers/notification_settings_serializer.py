from rest_framework import serializers
from mirrorGoal.models import NotificationSetting

class Serializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSetting
        fields = ['id', 'type', 'enabled']