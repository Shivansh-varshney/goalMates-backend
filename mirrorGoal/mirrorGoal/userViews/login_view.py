from rest_framework import status
from .renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from mirrorGoal.serializers.login_serializer import Serializer

def generate_token(user):
    refreshToken = RefreshToken.for_user(user)

    return {
        'access': str(refreshToken.access_token),
        'refresh': str(refreshToken)
    }


class View(APIView):

    renderer_classes = [UserRenderer]

    def post(self, request):

        serializer = Serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(email=email, password=password)

            if user:
                tokens = generate_token(user)
                return Response({
                    'status': 'success',
                    'tokens': tokens,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': 'error',
                    'message': 'Wrong credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)