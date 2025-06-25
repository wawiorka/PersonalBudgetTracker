from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BalanceView

router = DefaultRouter()
router.register(r'', BalanceView, basename='balances')

urlpatterns = [
    path('', include(router.urls)),
]