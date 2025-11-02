from rest_framework import status
from mirrorGoal.models import Goal
from .renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.user_goals_serializer import Serializer


class View(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goals = Goal.objects.filter(user=request.user).order_by('-completion_date')
        serializer = Serializer(goals, many=True)

        if goals.exists():
            return Response({
                'status': 'success',
                'message': 'Goals fetched successfully',
                'goals': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'success',
                'message': 'No Goals',
                'goals': []
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            return Response({
                'status': 'success',
                'message': 'Goal added successfully',
                'goal': serializer.validated_data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        goal_id = request.data.get('id')

        goalObj = get_object_or_404(Goal, id=goal_id, user=request.user)

        serializer = Serializer(goalObj, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Goal updated successfully',
                'goal': serializer.validated_data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        goal_id = request.data.get('id')

        goalObj = get_object_or_404(Goal, id=goal_id, user=request.user)

        if goalObj:
            goalObj.delete()

            return Response({
                'status': 'success',
                'message': 'Goal deleted successfully',
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Goal could not be found'
        }, status=status.HTTP_400_BAD_REQUEST)