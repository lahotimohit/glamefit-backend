from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed 
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User, OTPVerification
from .utils import get_tokens_for_user
import random

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            isVerified=False
        )
        otp = str(random.randint(100000, 999999))
        OTPVerification.objects.create(user=user, otp=otp)
        send_mail(
            'Your OTP Code',
            f'Your OTP for verification is {otp}.',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        return user
    

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        try:
            user = User.objects.get(email=email)
            otp_record = OTPVerification.objects.get(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'User not found'})
        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError({'otp': 'OTP not found'})

        if otp_record.is_expired():
            raise serializers.ValidationError({'otp': 'OTP expired'})

        if otp_record.otp != otp:
            raise serializers.ValidationError({'otp': 'Invalid OTP'})

        user.isVerified = True
        user.save()
        otp_record.delete()
        return {'message': 'User verified successfully'}
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid Credentials")

        token = get_tokens_for_user(user)
        return {
            "msg": "Login Successful...",
            "token": token
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'isVerified', 'isProfileComplete']