from django.shortcuts import render

from products.models import Category, Product


def home(request):
	categories = Category.objects.all()
	featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
	context = {
		"categories": categories,
		"featured_products": featured_products,
	}
	return render(request, "home.html", context)

# Create your views here.
