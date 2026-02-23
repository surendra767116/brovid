from django.contrib import admin

from .models import ColorOption, Category, Product, ProductImage, Review, SizeOption


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "stock", "is_featured", "is_active")
	list_filter = ("category", "is_featured", "is_active")
	search_fields = ("name", "category__name", "brand")
	prepopulated_fields = {"slug": ("name",)}
	filter_horizontal = ("available_sizes", "available_colors")
	inlines = [ProductImageInline]


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active", "sort_order")
	list_editable = ("is_active", "sort_order")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}
	ordering = ("sort_order", "name")


@admin.register(ColorOption)
class ColorOptionAdmin(admin.ModelAdmin):
	list_display = ("name", "hex_code", "is_active", "sort_order")
	list_editable = ("hex_code", "is_active", "sort_order")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}
	ordering = ("sort_order", "name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("product", "user", "rating", "created_at")
	list_filter = ("rating",)


admin.site.register(ProductImage)

# Register your models here.
