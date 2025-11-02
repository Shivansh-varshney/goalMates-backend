from mirrorGoal.models import User
from rest_framework import serializers
from taggit.managers import TaggableManager
from django.contrib.auth import authenticate

class Serializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=256)
    new_password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    interests = serializers.SerializerMethodField()
    interests_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone', 
                    'is_verified', 'location', 'user_timezone', 'interests', 'interests_input', 'old_password', 
                    'new_password', 'password', 'created_at', 'updated_at', 'bio']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        phone = validated_data.get('phone')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"username": "A user with this phone already exists."})

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests_input', None)

        userObj = super().update(instance, validated_data)

        if interests is not None:
            userObj.interests.set(interests)

        if 'new_password' in validated_data:
            new_password = validated_data['new_password']
            old_password = validated_data['old_password']

            user = authenticate(email=userObj.email, password=old_password)

            if user:
                user.set_password(new_password)
                user.save()
                return user
            raise serializers.ValidationError("Wrong password entered")

        if 'email' in validated_data:

            userObj.is_verified = False
            userObj.save()

        return userObj
    
    def get_interests(self, obj):
        return list(obj.interests.names())