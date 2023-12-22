from django.db import models
from django.contrib.auth import get_user_model
from carts.models import Cart
from django.db import models  # Import your user model
from products.models import Product
from django.contrib.auth.models import User


  # Import your product model

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other fields for order details (e.g., total amount, shipping details, etc.)

    def get_total_order_amount(self):
        # Method to calculate total order amount
        return sum(item.get_total_item_amount() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # Add other fields for order item details (e.g., price, total, etc.)

    def get_total_item_amount(self):
        # Method to calculate total amount for an order item
        return self.product.price * self.quantity
