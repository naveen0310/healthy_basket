from django.shortcuts import render
from .models import Order, OrderItem
from carts.models import  CartItem
from django.contrib.auth.decorators import login_required

def order_history(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'user_orders': user_orders})

# Implement further order-related views as needed
@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Create an order
        order = Order.objects.create(user=request.user)
        
        # Create order items based on cart items
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        
        # Clear the cart after creating the order
        cart_items.delete()
        
        return render(request, 'order_success.html', {'order': order})
    # Handle GET request to display checkout form
    # ...
@login_required
def view_orders(request):
    # Retrieve orders associated with the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Get orders, ordered by creation date
    
    return render(request, 'view_orders.html', {'orders': orders})
