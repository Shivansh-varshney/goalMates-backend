from rest_framework import serializers
from mirrorGoal.models import Message, MessageThread, User

class SenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    
    sender = SenderSerializer()

    class Meta:
        model = Message
        fields = '__all__'

class MessageThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = MessageThread
        fields = ['id', 'name', 'last_message']  # includes participants + last_message

    def get_name(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        
        other_user = obj.participants.exclude(id=request.user.id).first()
        return other_user.username if other_user else None

    def get_last_message(self, obj):
        last_msg = obj.message_set.order_by('-sent_at').first()
        if last_msg:
            return MessageSerializer(last_msg, context = self.context).data
        return None