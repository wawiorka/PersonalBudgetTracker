from django.contrib.admin import action
from rest_framework import serializers
from .models import Expense, ExpenseCategory


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context['request'].user
        expense = Expense.objects.create(**validated_data, user=user)
        return expense

