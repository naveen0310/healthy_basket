from django.urls import path,include
from . import views

urlpatterns = [
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.check_out, name='check_out'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-cart-item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('payments/', include('payments.urls')),
      # Add other cart-related URLs as needed
]
