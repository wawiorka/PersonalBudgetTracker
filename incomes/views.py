from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import IncomeCategory, Income
from .serializers import IncomeCategorySerializer, IncomeSerializer


# Create your views here.
class IncomeCategoryView(viewsets.ModelViewSet):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer
    # permission_classes = [IsAuthenticated]


class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
