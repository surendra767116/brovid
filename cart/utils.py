from django.shortcuts import get_object_or_404

from products.models import Product

from .models import Cart, CartItem


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_product_to_cart(user, product_id, quantity=1, size_label="", color_label=""):
    cart = get_user_cart(user)
    product = get_object_or_404(Product, id=product_id)
    quantity = max(1, quantity)
    normalized_size = size_label or ""
    normalized_color = color_label or ""
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        selected_size=normalized_size,
        selected_color=normalized_color,
    )
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return cart


def update_cart_item(user, item_id, quantity):
    cart = get_user_cart(user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return cart


def remove_cart_item(user, item_id):
    cart = get_user_cart(user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return cart
