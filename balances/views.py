from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Balance
from .serializers import BalanceSerializer


class BalanceView(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)