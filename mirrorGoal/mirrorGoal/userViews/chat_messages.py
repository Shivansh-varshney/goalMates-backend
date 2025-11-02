from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from mirrorGoal.models import Message
from mirrorGoal.serializers.message_serializers import MessageSerializer


class View(ListAPIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):

        thread_id = self.request.GET.get("thread_id")
        return Message.objects.filter(thread_id=thread_id).order_by('sent_at')
    
    def get(self, request):

        messages = self.get_queryset()
        
        serializer = self.get_serializer(messages, many=True)
        return Response({
            "stauts": "success",
            "message": "Chat messages fetched successfully",
            "new_chat": False if len(messages) else True,
            "chat_messages": serializer.data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request):

        message = get_object_or_404(Message, id=request.data.get('message_id'))
        serializer = self.get_serializer(message, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "message marked successfully",
            }, status=status.HTTP_200_OK)