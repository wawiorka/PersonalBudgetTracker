from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer


# Create your views here.
# class UserRegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({"user": serializer.data})
