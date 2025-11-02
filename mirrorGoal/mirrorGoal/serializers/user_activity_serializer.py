from rest_framework import serializers
from mirrorGoal.models import Activity

class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ['id', 'title', 'activityType', 'time', 'status']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)