from decimal import Decimal

from django.conf import settings
from django.db import models

from products.models import Product


class Cart(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="cart",
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self):
		return f"Cart for {self.user.username}"

	@property
	def items(self):
		return self.cart_items.select_related("product")

	@property
	def total_items(self):
		return sum(item.quantity for item in self.items)

	@property
	def total_amount(self):
		total = sum((item.subtotal for item in self.items), Decimal("0.00"))
		return total.quantize(Decimal("0.01"))


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	selected_size = models.CharField(max_length=60, blank=True)
	selected_color = models.CharField(max_length=60, blank=True)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-added_at"]
		constraints = [
			models.UniqueConstraint(
				fields=["cart", "product", "selected_size", "selected_color"],
				name="unique_cart_item_variant",
			)
		]

	def __str__(self):
		variant = self.variant_display
		return f"{self.product.name} {variant} ({self.quantity})"

	@property
	def subtotal(self):
		return self.product.price * self.quantity

	@property
	def variant_display(self):
		parts = [value for value in [self.selected_size, self.selected_color] if value]
		return f"({', '.join(parts)})" if parts else ""

# Create your models here.
