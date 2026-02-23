from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
	phone = models.CharField(max_length=20, blank=True)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to="profiles/", blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Profile of {self.user.username}"


class Wishlist(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
	products = models.ManyToManyField(Product, blank=True, related_name="wishlisted_by")
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Wishlist of {self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		Wishlist.objects.create(user=instance)

# Create your models here.
