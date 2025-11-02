import hashlib
from rest_framework import serializers
from mirrorGoal.models import EmailOTP

class Serializer(serializers.ModelSerializer):

    class Meta:
        model=EmailOTP
        fields=['otp']
        extra_kwargs={
            'otp':{
                'write_only': True
            }
        }

    def validate(self, attrs):

        user_email = self.context.get('email')
        user_otp = attrs.get('otp')

        try: 
            otpObj = EmailOTP.objects.filter(email=user_email).latest('createdAt')

            if hashlib.sha256(user_otp.encode()).hexdigest() == otpObj.otp:
                if not otpObj.is_expired():
                    attrs['otpObj'] = otpObj
                    return attrs
                    
                otpObj.delete()
                raise serializers.ValidationError("OTP expired.")
            raise serializers.ValidationError("Invalid OTP")

        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("OTP was not generated.")