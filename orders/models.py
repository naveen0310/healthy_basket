from django.db import models
from users.models import CustomUser
from carts.models import Cart

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # Add additional fields like total amount, shipping details, etc.
    created_at = models.DateTimeField(auto_now_add=True)
