from django.db import models
from django.contrib.auth import get_user_model
from carts.models import Cart

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # Add additional fields like total amount, shipping details, etc.
    created_at = models.DateTimeField(auto_now_add=True)
