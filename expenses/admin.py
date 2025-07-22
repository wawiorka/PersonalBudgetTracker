from django.contrib import admin

from .models import Expense, ExpenseCategory

# Register your models here.
# admin.site.register(Expense)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    exclude = ('user',) # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
