from rest_framework import serializers
from mirrorGoal.models import Goal, Achievement, UserAchievement

class GoalBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title']

class AchievementBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name']

class Serializer(serializers.ModelSerializer):

    achievement = AchievementBriefSerializer(read_only=True)
    goal = GoalBriefSerializer(read_only=True)

    achievement_id = serializers.PrimaryKeyRelatedField(
        queryset=Achievement.objects.all(),
        write_only=True,
        source='achievement'
    )
    goal_id = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.all(),
        write_only=True,
        source='goal'
    )

    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement_id', 'goal_id', 'achievement', 'goal']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)