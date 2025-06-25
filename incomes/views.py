from logging import raiseExceptions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import IncomeCategory, Income
from .serializers import IncomeCategorySerializer, IncomeSerializer
from balances.models import Balance


# Create your views here.
class IncomeCategoryView(viewsets.ModelViewSet):
    serializer_class = IncomeCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)


class IncomeView(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            balance = Balance.objects.filter(user=self.request.user)
            if len(balance) == 0:
                balance.create(value=serializer.validated_data.get('amount'),
                               type=1,
                               date=serializer.validated_data.get('date'),
                               user=self.request.user)
                return Response({'message': 'Личный бюджет начат.'}, status=status.HTTP_201_CREATED)
            elif len(balance) > 0:
                balance.update(value=F('value')+serializer.validated_data.get('amount'),
                               date=serializer.validated_data.get('date'))
                return Response({'message': 'Доход добавлен в бюджет.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

