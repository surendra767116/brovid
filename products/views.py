from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify

from orders.models import OrderItem

from .models import Category, ColorOption, Product, Review, SizeOption


def _update_recently_viewed(request, product_id):
	recently_viewed = request.session.get("recently_viewed_products", [])
	if product_id in recently_viewed:
		recently_viewed.remove(product_id)
	recently_viewed.insert(0, product_id)
	request.session["recently_viewed_products"] = recently_viewed[:10]


def _get_personalized_recommendations(request, current_product, limit=4):
	seen_ids = {current_product.id}
	recommendations = []

	if request.user.is_authenticated:
		purchased_items = OrderItem.objects.filter(
			order__user=request.user, product__isnull=False
		)
		purchased_product_ids = list(purchased_items.values_list("product_id", flat=True))
		seen_ids.update(purchased_product_ids)
		category_rankings = (
			purchased_items.values("product__category")
			.annotate(total=Count("product__category"))
			.order_by("-total")
		)
		for entry in category_rankings:
			if len(recommendations) >= limit:
				break
			category_id = entry["product__category"]
			if category_id is None:
				continue
			category_products = (
				Product.objects.filter(category_id=category_id, is_active=True)
				.exclude(id__in=seen_ids)
				.order_by("-is_featured", "-updated_at")
			)
			for product in category_products:
				recommendations.append(product)
				seen_ids.add(product.id)
				if len(recommendations) >= limit:
					break

	if len(recommendations) < limit:
		session_ids = [
			pk
			for pk in request.session.get("recently_viewed_products", [])
			if pk not in seen_ids
		]
		if session_ids:
			recent_products = Product.objects.filter(id__in=session_ids, is_active=True)
			recent_map = {product.id: product for product in recent_products}
			for pk in session_ids:
				if len(recommendations) >= limit:
					break
				product = recent_map.get(pk)
				if product:
					recommendations.append(product)
					seen_ids.add(product.id)

	if len(recommendations) < limit:
		fallback = (
			Product.objects.filter(is_active=True)
			.exclude(id__in=seen_ids)
			.order_by("-is_featured", "-created_at")[: limit - len(recommendations)]
		)
		recommendations.extend(list(fallback))

	return recommendations


def product_list(request):
	products = (
		Product.objects.filter(is_active=True)
		.select_related("category")
		.prefetch_related("available_sizes", "available_colors")
	)
	categories = Category.objects.all()
	size_options_qs = SizeOption.objects.filter(is_active=True).order_by("sort_order", "name")
	color_options_qs = ColorOption.objects.filter(is_active=True).order_by("sort_order", "name")
	size_options = list(size_options_qs)
	color_options = list(color_options_qs)

	category_slug = request.GET.get("category", "")
	min_price = request.GET.get("min_price", "")
	max_price = request.GET.get("max_price", "")
	size_filter = request.GET.get("size", "")
	color_filter = request.GET.get("color", "")
	search_query = request.GET.get("search", "")
	in_stock = request.GET.get("in_stock")

	if category_slug:
		products = products.filter(category__slug=category_slug)

	if min_price:
		products = products.filter(price__gte=min_price)
	if max_price:
		products = products.filter(price__lte=max_price)

	if size_filter:
		products = products.filter(
			Q(available_sizes__slug=size_filter)
			| Q(available_sizes__name__iexact=size_filter)
			| Q(size__iexact=size_filter)
		)

	if color_filter:
		products = products.filter(
			Q(available_colors__slug=color_filter)
			| Q(available_colors__name__iexact=color_filter)
			| Q(color__icontains=color_filter)
		)

	if in_stock in {"on", "true", "1"}:
		products = products.filter(stock__gt=0)

	if search_query:
		products = products.filter(
			Q(name__icontains=search_query)
			| Q(description__icontains=search_query)
			| Q(available_colors__name__icontains=search_query)
			| Q(brand__icontains=search_query)
		)

	if size_filter or color_filter or search_query:
		products = products.distinct()

	results_count = products.count()
	applied_filters = []
	if search_query:
		applied_filters.append({"label": "Search", "value": search_query})
	if category_slug:
		category_name = categories.filter(slug=category_slug).values_list("name", flat=True).first()
		applied_filters.append({"label": "Category", "value": category_name or category_slug})
	if min_price or max_price:
		price_label = f"₹{min_price or '0'} - ₹{max_price or '∞'}"
		applied_filters.append({"label": "Price", "value": price_label})
	if size_filter:
		size_label = next((option.name for option in size_options if option.slug == size_filter), size_filter)
		applied_filters.append({"label": "Size", "value": size_label})
	if color_filter:
		color_label = next((option.name for option in color_options if option.slug == color_filter), color_filter)
		applied_filters.append({"label": "Color", "value": color_label})
	if in_stock in {"on", "true", "1"}:
		applied_filters.append({"label": "Availability", "value": "In Stock"})

	context = {
		"products": products,
		"categories": categories,
		"search_query": search_query,
		"selected_category": category_slug,
		"selected_size": size_filter,
		"selected_color": color_filter,
		"min_price": min_price,
		"max_price": max_price,
		"in_stock_only": in_stock in {"on", "true", "1"},
		"results_count": results_count,
		"applied_filters": applied_filters,
		"size_options": size_options,
		"color_options": color_options,
	}
	return render(request, "products/list.html", context)


def category_detail(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = category.products.filter(is_active=True)
	categories = Category.objects.exclude(id=category.id)
	context = {
		"category": category,
		"products": products,
		"categories": categories,
	}
	return render(request, "products/category.html", context)


def product_detail(request, slug):
	product = get_object_or_404(
		Product.objects.prefetch_related("available_sizes", "available_colors", "images"),
		slug=slug,
		is_active=True,
	)
	_update_recently_viewed(request, product.id)
	reviews = product.reviews.select_related("user")
	avg_rating = reviews.aggregate(avg=Avg("rating"))
	avg_rating_value = avg_rating["avg"] or 0
	related_products = (
		Product.objects.filter(category=product.category, is_active=True)
		.exclude(id=product.id)
		[:4]
	)
	recommendations = _get_personalized_recommendations(request, product)
	size_options = [
		{"value": option.slug, "label": option.name}
		for option in product.available_sizes.filter(is_active=True)
	]
	if not size_options and product.size:
		size_options.append(
			{"value": product.size.lower(), "label": product.get_size_display()}
		)

	color_options = [
		{
			"value": option.slug,
			"label": option.name,
			"hex": option.hex_code,
		}
		for option in product.available_colors.filter(is_active=True)
	]
	if not color_options and product.color:
		color_options.append(
			{
				"value": slugify(product.color),
				"label": product.color,
			}
		)
	context = {
		"product": product,
		"reviews": reviews,
		"related_products": related_products,
		"avg_rating": avg_rating_value,
		"recommendations": recommendations,
		"size_options": size_options,
		"color_options": color_options,
	}
	return render(request, "products/detail.html", context)


def product_suggestions(request):
	query = request.GET.get("q", "").strip()
	results = []
	if query:
		suggestions = (
			Product.objects.filter(is_active=True)
			.filter(
				Q(name__icontains=query)
				| Q(available_colors__name__icontains=query)
				| Q(color__icontains=query)
				| Q(brand__icontains=query)
			)
			.order_by("name")
			.distinct()[:8]
		)
		results = [
			{
				"name": suggestion.name,
				"slug": suggestion.slug,
				"price": float(suggestion.price),
			}
			for suggestion in suggestions
		]
	return JsonResponse({"results": results})

# Create your views here.
