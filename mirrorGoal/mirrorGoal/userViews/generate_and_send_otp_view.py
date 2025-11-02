import random
import hashlib
from rest_framework import status
from .renderers import UserRenderer
from django.core.mail import send_mail
from mirrorGoal.models import EmailOTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class View(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        userObj = request.user
        # send email
        subject = "OTP for email confirmation on mirrorGoal."
        otp = str(random.randint(1000000, 9999999))
        print(f"\n{otp}\n")
        message = f"Use {otp} as the one-time password to verify your email and register on mirrorGoal."
        from_email = None
        recipient_list = [userObj.email]
        send_mail(subject, message, from_email, recipient_list)
        EmailOTP.objects.create(
            email=userObj.email,
            otp=hashlib.sha256(otp.encode()).hexdigest()
        )

        return Response({
                'status': 'success',
                'message': 'OTP sent successfully'
            }, status = status.HTTP_200_OK)