from rest_framework import status
from .renderers import UserRenderer
from mirrorGoal.models import CheckIn
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.user_checkins_serialier import Serializer

class View(GenericAPIView):

    serializer_class = Serializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return CheckIn.objects.filter(user=self.request.user, checked_in_at=None, missed=False)
    
    def get(self, request):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': 'success',
            'message': 'checkins fetched successfully',
            'checkins': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
            return Response({
                'status': 'success',
                'message': 'Check-in created successfully',
                'checkin': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request):
        
        checkin = get_object_or_404(CheckIn, id=request.data.get('checkin_id'))
        serializer = self.get_serializer(checkin, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Check-in updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)