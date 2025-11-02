from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.models import Activity
from django.shortcuts import get_object_or_404
from mirrorGoal.serializers.user_activity_serializer import Serializer

class View(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Serializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return Activity.objects.filter(user = self.request.user, status='Pending')
    
    def get(self, request):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'Activities fetched successfully',
            'activities': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request): 

        serializer = self.get_serializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Activity created successfully',
            }, status = status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        
        acitivity = get_object_or_404(Activity, id=request.data.get('activity_id'))
        serializer = self.get_serializer(acitivity, data=request.data, partial=True)
        print(serializer)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Activity updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)