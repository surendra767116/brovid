from django.contrib import admin

from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ("full_name", "user", "city", "is_default")
	list_filter = ("is_default", "city")
	search_fields = ("full_name", "city", "state", "user__username")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("order_number", "user", "status", "total_amount", "placed_at")
	list_filter = ("status", "placed_at")
	search_fields = ("order_number", "user__username")
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("order", "product_name", "quantity", "price")

# Register your models here.
