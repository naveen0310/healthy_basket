from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem, Product
from django.shortcuts import render, redirect
from .models import CartItem
from django.contrib.auth.decorators import login_required

def view_cart(request):
    # Retrieve the user's cart and cart items
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def check_out(request):
    # Retrieve the user's cart and cart items
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    overall_total = 0
    item_count=0
    for item in cart_items:
        item.total_amount = item.product.price * item.quantity
        item_count+=item.quantity
        overall_total += item.total_amount
        item.save()
    return render(request, 'checkout.html', {'cart_items': cart_items, 'overall_total': overall_total, 'item_count': item_count})
# Implement cart update, remove item, and checkout views as needed
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=product,
            user=request.user,
            defaults={'quantity': 1}  # Default quantity if the item is new in the cart
        )

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('view_cart')
    
@login_required
def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
        new_quantity = int(request.POST.get('quantity'))

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is set to 0 or less

        return redirect('view_cart')

@login_required
def remove_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
        cart_item.delete()

        return redirect('view_cart')