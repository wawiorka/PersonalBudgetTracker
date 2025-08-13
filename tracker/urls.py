from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import start_window

urlpatterns = [
    path('', start_window),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('incomes.urls')),
    path('balances/', include('balances.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
