from django.shortcuts import render

from products.models import Category, Product


def home(request):
	categories = Category.objects.all()
	recent_products = (
		Product.objects.filter(is_active=True)
		.select_related("category")
		.order_by("-created_at")[:8]
	)
	context = {
		"categories": categories,
		"recent_products": recent_products,
	}
	return render(request, "home.html", context)

# Create your views here.
