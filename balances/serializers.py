from rest_framework import serializers

from .models import Balance


class BalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Balance
        fields = '__all__'
        read_only_fields = ["user"]


    def create(self, validated_data):
        user = self.context['request'].user
        return Balance.objects.create(**validated_data, user=user)
    #
    # class BalanceTypeSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Balance.type
    #