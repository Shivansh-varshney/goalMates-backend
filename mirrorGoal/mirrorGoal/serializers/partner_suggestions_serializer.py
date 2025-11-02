from rest_framework import serializers

class Serializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    location = serializers.CharField(allow_null=True, required=False, read_only=True)
    bio = serializers.CharField(allow_null=True, required=False, read_only=True)
    count = serializers.IntegerField(read_only=True)
    goals = serializers.ListField(child=serializers.CharField(), read_only=True)
    interests = serializers.ListField(child=serializers.CharField(), read_only=True)
