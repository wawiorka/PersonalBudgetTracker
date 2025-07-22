from rest_framework import serializers
from .models import IncomeCategory, Income
from balances.models import Balance
from balances.serializers import BalanceSerializer


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ["user"]


    def create(self, validated_data):
        user = self.context['request'].user
        return Income.objects.create(**validated_data, user=user)
