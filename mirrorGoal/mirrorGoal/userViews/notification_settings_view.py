from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from mirrorGoal.models import NotificationSetting
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.notification_settings_serializer import Serializer


class View(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Serializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return NotificationSetting.objects.filter(user=self.request.user)
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'message': 'Settings fetched successfully',
            'settings': serializer.data
            }, status=status.HTTP_200_OK)
    
    def patch(self, request):
        
        try:
            data = request.data
            setting = NotificationSetting.objects.get(user=request.user, type=data.get('type'))
            serializer = self.get_serializer(setting, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Setting updated',
                    'setting': serializer.data
                    }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except NotificationSetting.DoesNotExist:
            return Response({
                'status': 'success',
                'message': 'No setting found'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response({
                'status': 'success',
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)