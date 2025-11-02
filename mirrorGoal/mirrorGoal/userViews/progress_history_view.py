from rest_framework import status
from mirrorGoal.models import Goal
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.progress_history_serializer import Serializer

class View(GenericAPIView):

    serializer_class = Serializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).prefetch_related('history')

    def get(self, request):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Goals history retrieved successfully',
            'goals': serializer.data
        }, status=status.HTTP_200_OK)