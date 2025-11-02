from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.models import Achievement, UserAchievement
from mirrorGoal.serializers.user_achievement_serializer import Serializer

class View(GenericAPIView):

    serializer_class = Serializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user)
    
    def get(self, request):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'User achievements fetched successfully',
            'achievements': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = self.get_serializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'User Achievement unlocked',
                'achievment': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )