from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import reverse, get_object_or_404
from google.oauth2 import id_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db import transaction
from . import serializers
from .models import BillingDetails

User = get_user_model()

class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = f"https://glamefit.netlify.app/auth/newPassword/{user.id}/{token}/"

            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent to email"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        token = kwargs.get('token')

        user = get_object_or_404(User, id=user_id)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

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
    

class BillingDetailsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer=serializers.BillingDetailsSerailizer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            billing_detail = serializer.save(user=request.user)
            request.user.default_billing_address = billing_detail
            request.user.save(update_fields=['default_billing_address'])
            return Response({"message": "Details saved successfully...."}, status=201)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            addresses = BillingDetails.objects.filter(user=request.user)
            serialized_data = serializers.BillingDetailsSerailizer(addresses, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        billing_id = request.data.get("billing_id")
        if not billing_id:
            return Response({'error': "billing_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        billing_detail = BillingDetails.objects.filter(id=billing_id, user=request.user).first()
        if not billing_detail:
            return Response({'error': "Billing detail not found"}, status=status.HTTP_404_NOT_FOUND)

        billing_detail.delete()
        return Response({"message": "Billing detail deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        billing_id = request.data.get("billing_id")
        if not billing_id:
            return Response({'error': "billing_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        billing_detail = BillingDetails.objects.filter(id=billing_id, user=request.user).first()
        if not billing_detail:
            return Response({'error': "Billing detail not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BillingDetailsSerailizer(billing_detail, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Billing detail updated successfully."}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)