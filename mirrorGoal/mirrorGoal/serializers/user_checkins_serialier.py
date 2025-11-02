from rest_framework import serializers
from mirrorGoal.models import CheckIn, Goal, ProgressHistory

class GoalBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title']

class Serializer(serializers.ModelSerializer):

    goal = GoalBriefSerializer(read_only=True)   # For GET
    goal_id = serializers.PrimaryKeyRelatedField(  # For POST/PUT
        queryset=Goal.objects.all(),
        source='goal',
        write_only=True
    )

    class Meta:
        model = CheckIn
        fields = ['id', 'goal', 'goal_id', 'scheduled_for', 'checked_in_at', 'missed']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        
        checkin = super().update(instance, validated_data)

        if 'checked_in_at' in validated_data:
            goal = checkin.goal
            ProgressHistory.objects.create(goal=goal, progress=goal.progress)

        return checkin