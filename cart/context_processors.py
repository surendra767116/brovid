from .utils import get_user_cart


def cart_summary(request):
    """Provide cart totals for navbar display."""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        return {
            "cart_total_items": cart.total_items,
            "cart_total_amount": cart.total_amount,
            "cart_items_count": cart.total_items,
        }
    return {"cart_total_items": 0, "cart_total_amount": 0, "cart_items_count": 0}
