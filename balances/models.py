from django.db import models

from users.models import User

# Create your models here.
class Balance(models.Model):
    class BalanceType(models.IntegerChoices):
        CUR = 1, "Текущие"
        SAV = 2, "Накопленные"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=BalanceType.choices, default=1)
    date = models.DateField()

    def __str__(self):
        return f'Balance {self.id} - {self.type}'