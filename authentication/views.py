from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
import jwt
from .serializer import UserSerializer
from django.conf import settings
from datetime import datetime, timedelta  # For setting token expiry

class RegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.ListAPIView):

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        #Send Res

        auth_token = jwt.encode(
            {'username': user.username, },
            settings.JWT_SECRET_KEY
        )

        serializer = UserSerializer(user)
        data = {
            "user": serializer.data, "token": auth_token
        }

        return Response(data, status=status.HTTP_200_OK)
