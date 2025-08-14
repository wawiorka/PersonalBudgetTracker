from django.db import models

from users.models import User

from tracker import settings


# Create your models here.
class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes_category')

    def __str__(self):
        return f"{self.amount} - {self.date} - {self.category}"

    class Meta:
        ordering = ['-date']
