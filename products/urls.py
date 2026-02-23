from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="list"),
    path("suggestions/", views.product_suggestions, name="suggestions"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("<slug:slug>/", views.product_detail, name="detail"),
]
