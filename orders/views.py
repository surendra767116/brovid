from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.utils import get_user_cart

from .forms import AddressForm
from .models import Address, Order, OrderItem


@login_required
def addresses(request):
	addresses = request.user.addresses.all()
	return render(request, "orders/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
	if request.method == "POST":
		form = AddressForm(request.POST)
		if form.is_valid():
			address = form.save(commit=False)
			address.user = request.user
			if address.is_default:
				request.user.addresses.update(is_default=False)
			address.save()
			messages.success(request, "Address saved successfully.")
			return redirect("orders:addresses")
	else:
		form = AddressForm()
	return render(request, "orders/address_form.html", {"form": form, "title": "Add Address"})


@login_required
def edit_address(request, pk):
	address = get_object_or_404(Address, pk=pk, user=request.user)
	if request.method == "POST":
		form = AddressForm(request.POST, instance=address)
		if form.is_valid():
			address = form.save(commit=False)
			address.user = request.user
			if address.is_default:
				request.user.addresses.exclude(pk=address.pk).update(is_default=False)
			address.save()
			messages.success(request, "Address updated successfully.")
			return redirect("orders:addresses")
	else:
		form = AddressForm(instance=address)
	return render(
		request,
		"orders/address_form.html",
		{"form": form, "title": "Edit Address"},
	)


@login_required
def delete_address(request, pk):
	address = get_object_or_404(Address, pk=pk, user=request.user)
	address.delete()
	messages.info(request, "Address removed.")
	return redirect("orders:addresses")


@login_required
def checkout(request):
	cart = get_user_cart(request.user)
	if not cart.items.exists():
		messages.warning(request, "Your cart is empty.")
		return redirect("products:list")

	addresses = request.user.addresses.all()
	if not addresses:
		messages.info(request, "Add an address before checkout.")
		return redirect("orders:add_address")

	shipping_estimate = Decimal("0.00") if cart.total_amount >= Decimal("999.00") else Decimal("49.00")
	order_total = cart.total_amount + shipping_estimate

	if request.method == "POST":
		address_id = request.POST.get("address")
		if not address_id:
			messages.error(request, "Please select a delivery address.")
			return redirect("orders:checkout")
		address = get_object_or_404(Address, pk=address_id, user=request.user)
		subtotal = cart.total_amount
		shipping = shipping_estimate
		total_amount = subtotal + shipping
		order = Order.objects.create(
			user=request.user,
			address=address,
			subtotal=subtotal,
			shipping=shipping,
			total_amount=total_amount,
		)
		for item in cart.items:
			OrderItem.objects.create(
				order=order,
				product=item.product,
				product_name=item.product.name,
				quantity=item.quantity,
				price=item.product.price,
				size_label=item.selected_size,
				color_label=item.selected_color,
			)
			item.product.stock = max(item.product.stock - item.quantity, 0)
			item.product.save()
		cart.cart_items.all().delete()
		messages.success(request, "Order placed successfully!")
		return redirect("orders:confirmation", order_number=order.order_number)

	return render(
		request,
		"orders/checkout.html",
		{
			"cart": cart,
			"addresses": addresses,
			"shipping_estimate": shipping_estimate,
			"order_total": order_total,
		},
	)


@login_required
def confirmation(request, order_number):
	order = get_object_or_404(Order, order_number=order_number, user=request.user)
	return render(request, "orders/confirmation.html", {"order": order})


@login_required
@require_POST
def cancel_order(request, order_number):
	order = get_object_or_404(Order, order_number=order_number, user=request.user)
	if not order.can_cancel:
		messages.warning(request, "This order can no longer be cancelled.")
		return redirect(request.POST.get("next") or "profiles:orders")

	order.status = "cancelled"
	order.save(update_fields=["status", "updated_at"])
	for item in order.items.select_related("product"):
		if item.product:
			item.product.stock = item.product.stock + item.quantity
			item.product.save(update_fields=["stock"])

	messages.success(request, f"Order {order.order_number} has been cancelled.")
	return redirect(request.POST.get("next") or "profiles:orders")

# Create your views here.
