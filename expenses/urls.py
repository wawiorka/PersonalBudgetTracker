from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expenses import views

from .views import ExpenseView, ExpenseCategoryView

router = DefaultRouter()
router.register(r'category', ExpenseCategoryView, basename='expense_category')
router.register(r'', ExpenseView, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    # path('create_category/', views.ExpenseCategoryCreateView.as_view(), name='expense_category_create'),
    # path('create/', views.ExpenseCreateView.as_view(), name='expense_create'),
]