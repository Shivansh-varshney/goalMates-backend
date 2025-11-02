from rest_framework import status
from .renderers import UserRenderer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.models import Notifications
from rest_framework.response import Response
from mirrorGoal.serializers.notifications_serializer import Serializer

class View(GenericAPIView):

    serializer_class = Serializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        userObj = self.request.user
        return Notifications.objects.filter(user = userObj)

    def get(self, request):
        
        notifications = self.get_queryset()

        serializer = self.get_serializer(notifications, many=True)

        return Response({
            "stauts": "success",
            "message": "notifications fetched successfully",
            "notifications": serializer.data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request):

        userObj = request.user
        notifications = Notifications.objects.filter(user = userObj, is_read=False)

        if notifications:
            updated_count = notifications.update(is_read=True)

            return Response({
                "status": "success",
                "message": f"{updated_count} notifications marked as read"
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "success",
            "message": f"Marked all as read"
        }, status=status.HTTP_200_OK)