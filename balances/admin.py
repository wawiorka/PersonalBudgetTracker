from django.contrib import admin

from .models import Balance

# Register your models here.
# admin.site.register(Balance)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "value", "type", "date")
    list_filter = ("user", "value", "type", "date")

admin.site.register(Balance, BalanceAdmin)