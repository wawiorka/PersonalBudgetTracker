from rest_framework import serializers
from .models import IncomeCategory, Income
from balances.models import Balance
from balances.serializers import BalanceSerializer


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    # balance = BalanceSerializer(many=True)
    class Meta:
        model = Income
        fields = '__all__'
