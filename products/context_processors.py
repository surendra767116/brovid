from .models import Category


def category_links(request):
    """Expose categories for global navigation menus."""
    categories = Category.objects.order_by("name")
    return {"nav_categories": categories}
