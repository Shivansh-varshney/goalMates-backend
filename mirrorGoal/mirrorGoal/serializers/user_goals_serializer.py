from mirrorGoal.models import Goal
from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from taggit.managers import TaggableManager

class TagListField(serializers.Field):
    def to_representation(self, value):
        # Works whether value is TaggableManager or a queryset
        if hasattr(value, "names"):
            return list(value.names())
        elif hasattr(value, "all"):
            return [tag.name for tag in value.all()]
        return []

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tag names.")
        return data

class Serializer(serializers.ModelSerializer):

    tags = TagListField(read_only=True)
    tags_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'progress', 'current_streak', 
                  'longest_streak', 'status', 'tags', 'tags_input', 'priority', 'completion_date', 
                  'created_at']
        
    def create(self, validated_data):
        # remove tags_input before creating Goal
        tags = validated_data.pop("tags_input", [])
        goal = Goal.objects.create(**validated_data)

        # assign tags if provided
        if tags:
            goal.tags.set(tags)   # TaggableManager works with set()
        return goal
    
    def update(self, instance, validated_data):

        goalObj = super().update(instance, validated_data)

        if 'progress' in validated_data:

            old_difference = goalObj.completion_date - goalObj.created_at.date()

            new_created_at = timezone.now()
            goalObj.created_at = new_created_at

            goalObj.completion_date = new_created_at.date() + old_difference

            goalObj.save()

        return goalObj