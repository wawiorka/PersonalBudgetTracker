from django.contrib import admin

from .models import Balance

# Register your models here.
# admin.site.register(Balance)

# class BalanceAdmin(admin.ModelAdmin):
#     list_display = ("user", "value", "type", "date")
#     list_filter = ("user", "value", "type", "date")
#
# admin.site.register(Balance, BalanceAdmin)

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    exclude = ('user',) # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)