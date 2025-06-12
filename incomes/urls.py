from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expenses import views

from .views import IncomeCategoryView, IncomeView

router = DefaultRouter()
router.register(r'category', IncomeCategoryView, basename='income_category')
router.register(r'', IncomeView, basename='incomes')

urlpatterns = [
    path('', include(router.urls)),
]