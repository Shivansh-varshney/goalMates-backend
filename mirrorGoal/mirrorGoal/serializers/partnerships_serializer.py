from rest_framework import serializers
from mirrorGoal.models import Partnership, User, Goal  # adjust import as needed

class GoalBreifSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ['id', 'title']

class UserBriefSerializer(serializers.ModelSerializer):

    goals = GoalBreifSerializer(many=True, read_only=True)
    interests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'interests', 'goals']

    def get_interests(self, obj):
        return list(obj.interests.names())

class Serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Partnership
        fields = ['id', 'user', 'accepted', 'created_at']

    def get_user(self, obj):
        """Return the 'other' user in this partnership."""
        request = self.context.get("request")
        current_user = request.user if request else None

        if current_user == obj.user_a:
            return UserBriefSerializer(obj.user_b).data
        return UserBriefSerializer(obj.user_a).data

