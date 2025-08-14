from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expenses import views

from .views import ExpenseView, ExpenseCategoryView, ExpenseDeleteView, ExpenseGraphView

router = DefaultRouter()
router.register(r'category', ExpenseCategoryView, basename='expense_category')
router.register(r'', ExpenseView, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>', ExpenseDeleteView.as_view(), name='expense_delete'),
    path("dashboard/user", views.graph_view, name = 'graph_view'),
    path('graph_view', ExpenseGraphView.as_view(),name="expense_graph_view"),
    # path('graph_view_by_time', ExpenseGraphViewByTime.as_view(),name="expense_graph_view_by_time"),
]