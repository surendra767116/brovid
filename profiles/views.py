from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import ProfileForm, UserForm


@login_required
def dashboard(request):
	recent_orders = request.user.orders.select_related("address")[:5]
	total_orders = request.user.orders.count()
	total_spent = sum((order.total_amount for order in request.user.orders.all()), Decimal("0.00"))
	wishlist_count = request.user.wishlist.products.count()
	context = {
		"recent_orders": recent_orders,
		"total_orders": total_orders,
		"total_spent": total_spent,
		"wishlist_count": wishlist_count,
	}
	return render(request, "profiles/dashboard.html", context)


@login_required
def orders_view(request):
	orders = request.user.orders.select_related("address")
	return render(request, "profiles/orders.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
	order = get_object_or_404(
		request.user.orders.select_related("address"),
		order_number=order_number,
	)
	order_items = order.items.select_related("product")
	return render(
		request,
		"profiles/order_detail.html",
		{"order": order, "order_items": order_items},
	)


@login_required
def settings_view(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, "Profile updated successfully.")
			return redirect("profiles:settings")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)

	context = {
		"user_form": user_form,
		"profile_form": profile_form,
	}
	return render(request, "profiles/settings.html", context)


@login_required
def change_password(request):
	from django.contrib.auth.forms import PasswordChangeForm
	from django.contrib.auth import update_session_auth_hash

	if request.method == "POST":
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, "Password updated successfully.")
			return redirect("profiles:settings")
	else:
		form = PasswordChangeForm(user=request.user)
	return render(request, "profiles/change_password.html", {"form": form})


@login_required
def wishlist_view(request):
	wishlist = request.user.wishlist
	return render(request, "profiles/wishlist.html", {"wishlist": wishlist})


@login_required
def add_to_wishlist(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	wishlist = request.user.wishlist
	wishlist.products.add(product)
	messages.success(request, f"{product.name} added to your wishlist.")
	return redirect(product.get_absolute_url())


@login_required
def remove_from_wishlist(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	wishlist = request.user.wishlist
	wishlist.products.remove(product)
	messages.info(request, f"{product.name} removed from your wishlist.")
	next_url = request.GET.get("next") or "profiles:wishlist"
	return redirect(next_url)

# Create your views here.
