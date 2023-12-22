from django.shortcuts import render, redirect
from .models import Cart, CartItem
#from payments.gateways import PaymentGateway
from orders.models import Order, OrderItem
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = 'sk_test_51OPstQSGtlmAVe1iw5tWehVv9QjHMFCbAz6VeoYF8TdPBcSAFhPQCyQPVqdLHx5uKJrYYmycUNE5sd23qVik37Ju00GiSC5d1v'
def calculate_total_amount(cart_items):
    total_amount = 0
    for cart_item in cart_items:
        total_amount += cart_item.product.price * cart_item.quantity
    return total_amount


@login_required
def process_payment(request):
    if request.method == 'POST':
        # Get the total amount to charge the customer
        total_amount = calculate_total_amount(CartItem.objects.filter(user=request.user))  # Calculate total amount
        
        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),  # Stripe requires the amount in cents
            currency='usd',  # Change currency as per your requirement
            metadata={'integration_check': 'accept_a_payment'},
        )
        
        # Create an order after successful payment
        intent.status='succeeded'
        if intent.status == 'succeeded':
            order = Order.objects.create(user=request.user)
            cart_items = CartItem.objects.filter(user=request.user)
            
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            
            cart_items.delete()  # Clear the cart after creating the order
            
            return render(request, 'order_success.html', {'order': order})
        else:
            return render(request, 'payment_failed.html')  # Render payment failed page
    # Handle other HTTP methods or cases as needed
    # ...

def checkout(request):
    # Retrieve the user's cart and cart items
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    
    # Calculate total amount from cart items
    
    # Process payment
    #payment_gateway = PaymentGateway()
    #payment_status = payment_gateway.process_payment(request.user, total_amount)
    payment_status=True
    
    if payment_status:
        # Create an order for the user
        order = Order.objects.create(user=request.user, cart=user_cart, total_amount=total_amount)
        # Additional logic like clearing the cart, sending confirmation email, etc.
        # Redirect to a success page or order confirmation page
        return redirect('order_confirmation', order_id=order.id)
    else:
        # Handle payment failure, show an error message to the user
        return render(request, 'payment_error.html')
