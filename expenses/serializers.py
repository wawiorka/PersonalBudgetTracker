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
        fields = ["id", "amount", "date", "user", "category"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context['request'].user
        expense = Expense.objects.create(**validated_data, user=user)
        return expense


class ExpenseDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ["user"]

    def delete(self, validated_data):
        user = self.context['request'].user
        expense = Expense.objects.get(**validated_data, user=user)
        return expense

class ExpenseGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date', 'user_id', 'category_id']


# class ExpenseGraphByTimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Expense
#         fields = ['id', 'amount', 'date', 'user_id', 'category_id']
#
#     def create(self, instance, validated_data):
#         instance.start_date = validated_data['start_date']
#         instance.end_date = validated_data['end_date']
#         return instance