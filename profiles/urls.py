from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("orders/", views.orders_view, name="orders"),
    path("orders/<str:order_number>/", views.order_detail, name="order_detail"),
    path("settings/", views.settings_view, name="settings"),
    path("change-password/", views.change_password, name="change_password"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]
