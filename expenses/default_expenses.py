from .models import ExpenseCategory

default_expenses = [
    ExpenseCategory(name='Еда', is_default=True),
    ExpenseCategory(name='Кафе', is_default=True),
    ExpenseCategory(name='Развлечения', is_default=True),
    ExpenseCategory(name='Транспорт', is_default=True),
    ExpenseCategory(name='Здоровье', is_default=True),
    ExpenseCategory(name='Питомцы', is_default=True),
    ExpenseCategory(name='Семья', is_default=True),
    ExpenseCategory(name='Одежда', is_default=True),
    ExpenseCategory(name='Коммуналка', is_default=True),
]
