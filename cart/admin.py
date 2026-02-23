from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ("user", "total_items", "total_amount", "updated_at")
	inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ("cart", "product", "quantity", "added_at")

# Register your models here.
