from django.contrib.admin import action
from rest_framework import serializers
from .models import Expense, ExpenseCategory
from tracker import settings


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
    #
    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     task = Task.objects.create(
    #         author=user,
    #         title=validated_data['title'],
    #         goal=validated_data['goal'])
    #     return task



class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     task = Task.objects.create(
    #         author=user,
    #         title=validated_data['title'],
    #         goal=validated_data['goal'])
    #     return task