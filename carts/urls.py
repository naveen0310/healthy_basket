from django.urls import path
from . import views

urlpatterns = [
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # Add other cart-related URLs as needed
]
