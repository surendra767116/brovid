import uuid

from django.conf import settings
from django.db import models

from products.models import Product


class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
	full_name = models.CharField(max_length=150)
	phone = models.CharField(max_length=20)
	address_line1 = models.CharField(max_length=255)
	address_line2 = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=100, default="India")
	is_default = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-is_default", "-updated_at"]

	def __str__(self):
		return f"{self.full_name} ({self.city})"


class Order(models.Model):
	STATUS_CHOICES = [
		("pending", "Pending"),
		("processing", "Processing"),
		("shipped", "Shipped"),
		("delivered", "Delivered"),
		("cancelled", "Cancelled"),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
	order_number = models.CharField(max_length=20, unique=True, editable=False)
	address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
	subtotal = models.DecimalField(max_digits=10, decimal_places=2)
	shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	placed_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	CANCELLABLE_STATUSES = {"pending", "processing"}

	class Meta:
		ordering = ["-placed_at"]

	def __str__(self):
		return self.order_number

	def save(self, *args, **kwargs):
		if not self.order_number:
			self.order_number = uuid.uuid4().hex[:10].upper()
		super().save(*args, **kwargs)

	@property
	def can_cancel(self):
		return self.status in self.CANCELLABLE_STATUSES


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	product_name = models.CharField(max_length=200)
	size_label = models.CharField(max_length=60, blank=True)
	color_label = models.CharField(max_length=60, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ["product_name"]

	def __str__(self):
		variant = self.variant_display
		return f"{self.product_name} {variant} x {self.quantity}"

	@property
	def total(self):
		return self.price * self.quantity

	@property
	def subtotal(self):
		return self.total

	@property
	def variant_display(self):
		parts = [value for value in [self.size_label, self.color_label] if value]
		return f"({', '.join(parts)})" if parts else ""

# Create your models here.
