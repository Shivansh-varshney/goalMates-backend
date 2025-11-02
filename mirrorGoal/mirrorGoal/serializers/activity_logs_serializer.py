from rest_framework import serializers
from mirrorGoal.models import Activity, User

class UserBreifSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class Serializer(serializers.ModelSerializer):

    is_current_user = serializers.SerializerMethodField()
    user = UserBreifSerializer()

    class Meta:
        model = Activity
        fields = ['id', 'title', 'user', 'activityType', 'time', 'is_current_user']

    def get_is_current_user(self, obj):
        request = self.context.get("request")
        return obj.user == request.user