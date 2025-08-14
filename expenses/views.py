import base64
import datetime
import io
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import floatformat
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView
from matplotlib import pyplot as plt
from rest_framework import viewsets, status, views, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from unicodedata import category

from .models import Expense, ExpenseCategory
from .serializers import ExpenseCategorySerializer, ExpenseSerializer, ExpenseGraphSerializer, \
    ExpenseGraphByTimeSerializer
from balances.models import Balance

from balances.serializers import BalanceSerializer


# Create your views here.
def graph_view(request):
    # Группируем расходы по категориям и суммируем для графика
    data = Expense.objects.filter(user=request.user
                                             ).values('category__name'
                                                      ).annotate(total_amount=Sum('amount')
                                                                 ).order_by('category')

    result = [{'category__name': item['category__name'], 'total_amount': float(item['total_amount'])} for item in data]
    return render(request, 'dashboard_expenses.html', {'data': result})


class ExpenseGraphView(APIView):
    '''Отображение расходов суммарно по категориям.'''
    permission_classes = [IsAuthenticated]


    def get(self, request):
        data = Expense.objects.filter(user=request.user
                                      ).values('category__name'
                                               ).annotate(total_amount=Sum('amount')
                                                          ).order_by('category')
        serializer = ExpenseGraphSerializer(data, many=True)
        result = [{'category__name': item['category__name'],
                   'total_amount': float(item['total_amount'])}
                  for item in data]

        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)


# class ExpenseGraphViewByTime(APIView):
#     '''Отображение расходов суммарно по категориям в указанный период времени.'''
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         serializer = ExpenseGraphByTimeSerializer(data=request.data, instance=instance)
#         user = self.request.user
#
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')
#
#         start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
#
#         expenses = Expense.objects.filter(date__range=[start_date, end_date])
#         grouped_expenses = expenses.values('category').annotate(total_amount=Sum('amount'))
#         result = list(grouped_expenses)
#
#         return JsonResponse(result, safe=False, status=status.HTTP_200_OK)


class ExpenseCategoryView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''CRUD по категориям расходов.'''
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = ExpenseCategory.objects.all()


class ExpenseView(mixins.CreateModelMixin,
                   # mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''Список расходов авторизованного пользователя. '''
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        '''Внести расход.'''
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

    # def update(self, request, *args, **kwargs):
    #     '''Обновить категорию расхода.'''
    #
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)


class ExpenseDeleteView(APIView):
    '''Удалить расход по id.'''
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            expense = Expense.objects.get(id=id, user=self.request.user)
            balance = Balance.objects.get(user=self.request.user, type=1)
            balance.value += expense.amount
            balance.save()
            expense.delete()
            return Response({'message': 'Расход удален.'}, status=status.HTTP_204_NO_CONTENT)

        except Expense.DoesNotExist:
            return Response({"error": "Расход (id) не найден."}, status=status.HTTP_404_NOT_FOUND)
