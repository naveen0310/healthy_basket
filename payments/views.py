from django.shortcuts import render, redirect
from .models import Cart, CartItem
from payments.gateways import PaymentGateway
from orders.models import Order

def checkout(request):
    # Retrieve the user's cart and cart items
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    
    # Calculate total amount from cart items
    
    # Process payment
    payment_gateway = PaymentGateway()
    payment_status = payment_gateway.process_payment(request.user, total_amount)
    
    if payment_status:
        # Create an order for the user
        order = Order.objects.create(user=request.user, cart=user_cart, total_amount=total_amount)
        # Additional logic like clearing the cart, sending confirmation email, etc.
        # Redirect to a success page or order confirmation page
        return redirect('order_confirmation', order_id=order.id)
    else:
        # Handle payment failure, show an error message to the user
        return render(request, 'payment_error.html')
