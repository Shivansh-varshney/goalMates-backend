from rest_framework import status
from .renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from mirrorGoal.serializers.user_data_serializer import Serializer

def generate_token(user):

    refreshToken = RefreshToken.for_user(user)

    return {
        'access': str(refreshToken.access_token),
        'refresh': str(refreshToken)
    }

class View(APIView):

    renderer_classes = [UserRenderer]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        serializer = Serializer(request.user)

        return Response({
            'status': 'success',
            'message': 'User fetched successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = Serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            
            userObj=serializer.save()
            tokens = generate_token(userObj)

            return Response({
                'status': 'success',
                'tokens': tokens,
                'message': 'User registered successfully',
                'user': serializer.data
            }, status = status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        userObj = request.user

        if userObj:
            serializer = Serializer(userObj, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                'status': 'success',
                'message': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(
                serializer.errros,
                status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        
        userObj = request.user
        userObj.delete()

        return Response({
            'status': 'success',
            'message': 'User deleted successfully'
        }, status=status.HTTP_200_OK)