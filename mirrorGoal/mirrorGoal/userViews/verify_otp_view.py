from rest_framework import status
from .renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.verify_email_otp_serializer import Serializer



class View(APIView):

    renderer_classes=[UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer(data=request.data, context={'email': request.user.email})
        
        if serializer.is_valid(raise_exception=True):
            otpObj = serializer.validated_data['otpObj']
            otpObj.delete()

            userObj = request.user
            userObj.is_verified = True
            userObj.save()

        return Response({
                'status': 'success',
                'message': 'OTP verification successfull'
            }, status=status.HTTP_202_ACCEPTED)