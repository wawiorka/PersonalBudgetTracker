from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView
from rest_framework import viewsets, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Expense, ExpenseCategory
from .serializers import ExpenseCategorySerializer, ExpenseSerializer
from balances.models import Balance

from balances.serializers import BalanceSerializer


# Create your views here.
class ExpenseCategoryView(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                balance=Balance.objects.get(user=self.request.user, type=1)
                if balance.value >= serializer.validated_data.get('amount'):
                    serializer.save()
                    Balance.objects.filter(user=self.request.user,
                                           type=1).update(value=F('value') - serializer.validated_data.get('amount'),
                                                          date=serializer.validated_data.get('date') or timezone.now())
                    return Response({'message': 'Расход учтен в бюджете.'}, status=status.HTTP_201_CREATED)
                if balance.value < serializer.validated_data.get('amount'):
                    return Response({'message': 'В текущем бюджете не хватает средств.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, *args, **kwargs):
    #     serializer = ExpenseSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         with transaction.atomic():
    #             balance=Balance.objects.get(user=self.request.user, type=1)
    #             if balance.value >= serializer.validated_data.get('amount'):
    #                 serializer.save()
    #                 Balance.objects.filter(user=self.request.user,
    #                                        type=1).update(value=F('value') - serializer.validated_data.get('amount'),
    #                                 date=serializer.validated_data.get('date'))
    #                 return Response({'message': 'Расход учтен в бюджете.'}, status=status.HTTP_201_CREATED)
    #             if balance.value < serializer.validated_data.get('amount'):
    #                 return Response({'message': 'В текущем бюджете не хватает средств.'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

