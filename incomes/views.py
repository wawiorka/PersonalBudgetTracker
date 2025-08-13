from logging import raiseExceptions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import IncomeCategory, Income
from .serializers import IncomeCategorySerializer, IncomeSerializer, IncomeGraphSerializer
from balances.models import Balance


# Create your views here.
def graph_view(request):
    # Группируем доходы по категориям и суммируем для графика
    data = Income.objects.filter(user=request.user
                                             ).values('category__name'
                                                      ).annotate(total_amount=Sum('amount')
                                                                 ).order_by('category')

    result = [{'category__name': item['category__name'], 'total_amount': float(item['total_amount'])} for item in data]
    return render(request, 'dashboard_incomes.html', {'data': result})


class IncomeGraphView(APIView):
    '''Отображение расходов суммарно по категориям.'''
    permission_classes = [IsAuthenticated]


    def get(self, request):
        data = Income.objects.filter(user=request.user
                                      ).values('category__name'
                                               ).annotate(total_amount=Sum('amount')
                                                          ).order_by('category')
        serializer = IncomeGraphSerializer(data, many=True)
        result = [{'category__name': item['category__name'],
                   'total_amount': float(item['total_amount'])}
                  for item in data]

        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)


class IncomeCategoryView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''CRUD по категориям доходов авторизованного пользователя.'''
    serializer_class = IncomeCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)


class IncomeView(mixins.CreateModelMixin,
                   # mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''Список доходов авторизованного пользователя. '''
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        '''Внести доход.'''
        serializer = IncomeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                balance = Balance.objects.filter(user=self.request.user, type=1)
                if len(balance) == 0:
                    serializer.save()
                    balance.create(value=serializer.validated_data.get('amount'),
                                   type=1,
                                   date=serializer.validated_data.get('date') or timezone.now(),
                                   user=self.request.user)
                    return Response({'message': 'Личный бюджет начат.'}, status=status.HTTP_201_CREATED)
                elif len(balance) > 0:
                    serializer.save()
                    balance.update(value=F('value')+serializer.validated_data.get('amount'),
                                   date=serializer.validated_data.get('date') or timezone.now())
                    return Response({'message': 'Доход добавлен в бюджет.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class IncomeDeleteView(APIView):
    '''Удалить расход по id.'''
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            income = Income.objects.get(id=id, user=self.request.user)
            balance = Balance.objects.get(user=self.request.user, type=1)
            balance.value -= income.amount
            balance.save()
            income.delete()
            return Response({'message': 'Доход удален.'}, status=status.HTTP_204_NO_CONTENT)

        except Income.DoesNotExist:
            return Response({"error": "Доход (id) не найден."}, status=status.HTTP_404_NOT_FOUND)