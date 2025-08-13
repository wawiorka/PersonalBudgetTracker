from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import IncomeCategoryView, IncomeView, IncomeDeleteView, IncomeGraphView

router = DefaultRouter()
router.register(r'category', IncomeCategoryView, basename='income_category')
router.register(r'', IncomeView, basename='incomes')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>', IncomeDeleteView.as_view(), name='income_delete'),
    path("dashboard/user", views.graph_view, name = 'income_graph_view'),
    path('graph_view', IncomeGraphView.as_view(),name="income_graph_view"),
]