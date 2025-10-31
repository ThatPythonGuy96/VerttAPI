from django.shortcuts import render
from . import models, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework import status, generics, permissions
from rest_framework.response import Response

@extend_schema(tags=["Account"])
class LoginView(TokenObtainPairView):
    serializer_class = serializers.LoginTokenSerializer

@extend_schema(tags=["Account"])
class SignupApi(APIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(tags=["Account"])
class BuyerView(APIView):
    serializer_class = serializers.BuyerSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        account = self.request.user
        buyer = models.Buyer.objects.get(account=account)
        serializer = serializers.BuyerSerializer(buyer)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Account"])
class AccountView(APIView):
    serializer_class = serializers.AccountSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        account_ = self.request.user.id
        account = models.Account.objects.get(id=account_)
        serializer = serializers.AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)