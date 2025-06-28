from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.
# class BalanceType(models.Model):
#     name = models.CharField(max_length=50)
#     date_created = models.DateField(default=timezone.now)
#     is_default = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
#

class Balance(models.Model):
    class BalanceType(models.IntegerChoices):
        CUR = 1, "Текущий"
        SAV = 2, "Накопления"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=BalanceType.choices, default=1)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'User: {self.user}, balance: {self.value} - type {self.type}'