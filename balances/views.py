from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Balance
from .serializers import BalanceSerializer


class BalanceView(viewsets.ViewSet):
    """Перенос денежной суммы внутри баланса:
    на текущий счет - 1;
    на накопления - 2"""
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = BalanceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            balance = Balance.objects.filter(user=self.request.user)

            """если хотим переместить с накоплений (2) на текущий (1)"""
            if serializer.validated_data.get('type') == 1:
                balance.filter(type=1).update(value=F('value') + serializer.validated_data.get('value'),
                                              date=serializer.validated_data.get('date') or timezone.now())
                balance.filter(type=2).update(value=F('value') - serializer.validated_data.get('value'),
                                              date=serializer.validated_data.get('date') or timezone.now())
                return Response({'message': 'Текущий баланс пополнен, накопления уменьшены.'},
                                status=status.HTTP_201_CREATED)

            """если хотим переместить в накопления (2)"""
            if serializer.validated_data.get('type') == 2:
                balance.filter(type=1).update(value=F('value') - serializer.validated_data.get('value'),
                                              date=serializer.validated_data.get('date') or timezone.now())
                if len(balance.filter(type=2)) == 0:
                    balance.create(value=serializer.validated_data.get('value'),
                                   type=2,
                                   date=serializer.validated_data.get('date') or timezone.now(),
                                   user=self.request.user)
                else:
                    balance.filter(type=2).update(value=F('value') + serializer.validated_data.get('value'),
                                   date=serializer.validated_data.get('date') or timezone.now(),
                                   user=self.request.user)
                return Response({'message': 'Накопление добавлено.'},
                                status=status.HTTP_201_CREATED)
