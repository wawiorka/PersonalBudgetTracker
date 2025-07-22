from django.contrib import admin

from .models import Income, IncomeCategory

# Register your models here.
# admin.site.register(Income)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    exclude = ('user',) # скрыть поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)