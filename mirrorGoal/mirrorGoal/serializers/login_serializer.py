from mirrorGoal.models import User
from rest_framework import serializers

class Serializer(serializers.ModelSerializer):

    email=serializers.EmailField(max_length=256)
    class Meta:
        model=User
        fields=['email', 'password']

    