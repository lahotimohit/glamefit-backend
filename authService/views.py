from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers


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