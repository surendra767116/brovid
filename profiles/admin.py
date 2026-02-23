from django.contrib import admin

from .models import Profile, Wishlist


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "phone", "updated_at")
	search_fields = ("user__username", "phone")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
	list_display = ("user", "updated_at")

# Register your models here.
