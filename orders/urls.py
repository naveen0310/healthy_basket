from django.urls import path, include
from . import views

urlpatterns = [
    path('view-orders/', views.view_orders, name='view_orders'),
]
