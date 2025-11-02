from rest_framework import status
from mirrorGoal.admin import User
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import OuterRef, Subquery
from mirrorGoal.models import MessageThread, Message
from mirrorGoal.serializers.message_serializers import MessageThreadSerializer


class View(ListAPIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageThreadSerializer

    def get_queryset(self):

        userObj = self.request.user

        # Subquery: for each thread, get the latest sent_at from related messages
        latest_message = Message.objects.filter(
            thread=OuterRef("pk")
        ).order_by("-sent_at")

        return (
            MessageThread.objects.filter(participants=userObj)
            .annotate(last_message_time=Subquery(latest_message.values("sent_at")[:1]))
            .order_by("-last_message_time")  # newest first
        )
  
    def get(self, request):
        
        messageThreads = self.get_queryset()
        serializer = self.get_serializer(messageThreads, many=True)

        return Response({
            "status": "success",
            "message": "Threads fetched successfully",
            "threads": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        partner_id = request.data.get("partner_id")
        user = request.user

        try:
            partner = User.objects.get(id=partner_id)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Partner not found"
            }, status=status.HTTP_404_NOT_FOUND)

        existing_thread = (
            MessageThread.objects
            .filter(participants=user)
            .filter(participants=partner)
            .distinct()
            .first()
        )

        if existing_thread:
            thread = existing_thread
        else:
            thread = MessageThread.objects.create()
            thread.participants.add(user, partner)

        serializer = self.get_serializer(thread)

        return Response({
            "status": "success",
            "thread": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request):

        thread_id = request.data.get("thread_id")

        thread = MessageThread.objects.get(id=thread_id)

        thread.delete()

        return Response({
            "status": "success",
            "message": "Chat deleted successfully"
        }, status=status.HTTP_200_OK)