from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(max_length=140, unique=True, blank=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("products:category", args=[self.slug])



class SizeOption(models.Model):
	name = models.CharField(max_length=40, unique=True)
	slug = models.SlugField(max_length=60, unique=True, blank=True)
	sort_order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class ColorOption(models.Model):
	name = models.CharField(max_length=60, unique=True)
	slug = models.SlugField(max_length=80, unique=True, blank=True)
	hex_code = models.CharField(max_length=7, blank=True, help_text="#rrggbb format")
	sort_order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sort_order", "name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Product(models.Model):
	SIZE_CHOICES = [
		("XS", "Extra Small"),
		("S", "Small"),
		("M", "Medium"),
		("L", "Large"),
		("XL", "Extra Large"),
		("XXL", "2XL"),
	]

	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True, blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	size = models.CharField(max_length=4, choices=SIZE_CHOICES, default="M")
	color = models.CharField(max_length=60, blank=True)
	brand = models.CharField(max_length=100, blank=True)
	image = models.ImageField(upload_to="products/main/", blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True, help_text="Uncheck to hide from shop")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	available_sizes = models.ManyToManyField(SizeOption, blank=True, related_name="products")
	available_colors = models.ManyToManyField(ColorOption, blank=True, related_name="products")

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	@property
	def is_in_stock(self):
		return self.stock > 0 and self.is_active

	def get_absolute_url(self):
		return reverse("products:detail", args=[self.slug])


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
	image = models.ImageField(upload_to="products/gallery/")
	alt_text = models.CharField(max_length=120, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["id"]

	def __str__(self):
		return f"{self.product.name} image"


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(default=5)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
		unique_together = ("product", "user")

	def __str__(self):
		return f"Review for {self.product} by {self.user}"

# Create your models here.
