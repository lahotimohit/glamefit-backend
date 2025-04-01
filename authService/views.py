from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from google.oauth2 import id_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db import transaction
from . import serializers

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = serializers.GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        id_token_str = serializer.validated_data.get('token')
        
        try:
            client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), client_id)
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            profile_pic = idinfo.get('picture', '')
            
            with transaction.atomic():
                try:
                    social_account = SocialAccount.objects.get(provider='google', uid=google_id)
                    user = social_account.user
                except SocialAccount.DoesNotExist:
                    try:
                        user = User.objects.get(email=email)
                    except User.DoesNotExist:
                        username = email.split('@')[0]
                        base_username = username
                        counter = 1
                        
                        while User.objects.filter(username=username).exists():
                            username = f"{base_username}{counter}"
                            counter += 1
                        
                        user = User.objects.create_user(
                            email=email,
                        )
                    
                    # Create social account
                    SocialAccount.objects.create(
                        user=user,
                        provider='google',
                        uid=google_id,
                        extra_data=idinfo
                    )
            
                token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "OTP sent successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = serializers.OTPVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            serializer = serializers.UserProfileSerializer(user)
            return Response({"msg": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class GoogleLoginAPIView(APIView):
    def get(self, request):
        google_login_url = (
            f"{request.scheme}://{request.get_host()}"
            + reverse("account_login")
            + "?process=login&provider=google"
        )
        return Response({"google_login_url": google_login_url})
    