from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

# Create your views here.
User = get_user_model()

# User = get_user_model()

# class ObtainTokenPairView()

class Login(APIView):
    def post(self, request):
        print(request.data)
        return Response({"message" : "success"}, status=status.HTTP_200_OK)



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return Response(request.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

