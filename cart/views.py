from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from products.models import Product

from .utils import add_product_to_cart, get_user_cart, remove_cart_item, update_cart_item


@login_required
def cart_detail(request):
	cart = get_user_cart(request.user)
	return render(request, "cart/cart.html", {"cart": cart})


@login_required
def add(request, product_id):
	product = get_object_or_404(
		Product.objects.prefetch_related("available_sizes", "available_colors"),
		id=product_id,
		is_active=True,
	)
	quantity = int(request.POST.get("quantity", 1))
	size_slug = request.POST.get("size", "").strip()
	color_slug = request.POST.get("color", "").strip()
	size_label = ""
	color_label = ""

	available_sizes = product.available_sizes.filter(is_active=True)
	available_colors = product.available_colors.filter(is_active=True)

	if available_sizes.exists():
		size_option = available_sizes.filter(slug=size_slug).first()
		if not size_option:
			messages.error(request, "Please choose a size before adding to cart.")
			return redirect(product.get_absolute_url())
		size_label = size_option.name
	elif size_slug:
		size_map = {code: label for code, label in Product.SIZE_CHOICES}
		size_label = size_map.get(size_slug.upper(), size_slug)

	if available_colors.exists():
		color_option = available_colors.filter(slug=color_slug).first()
		if not color_option:
			messages.error(request, "Please choose a color before adding to cart.")
			return redirect(product.get_absolute_url())
		color_label = color_option.name
	elif color_slug:
		if product.color and slugify(product.color) == color_slug:
			color_label = product.color
		else:
			color_label = color_slug

	add_product_to_cart(request.user, product.id, quantity, size_label, color_label)
	messages.success(request, f"Added {product.name} to your cart.")
	next_url = request.POST.get("next") or product.get_absolute_url()
	return redirect(next_url)


@login_required
def update(request, item_id):
	quantity = int(request.POST.get("quantity", 1))
	update_cart_item(request.user, item_id, quantity)
	messages.success(request, "Cart updated successfully.")
	return redirect("cart:view")


@login_required
def remove(request, item_id):
	remove_cart_item(request.user, item_id)
	messages.info(request, "Item removed from cart.")
	return redirect("cart:view")

# Create your views here.
