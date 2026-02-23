from django.urls import path

from . import views

urlpatterns = [
    path("addresses/", views.addresses, name="addresses"),
    path("addresses/add/", views.add_address, name="add_address"),
    path("addresses/<int:pk>/edit/", views.edit_address, name="edit_address"),
    path("addresses/<int:pk>/delete/", views.delete_address, name="delete_address"),
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<str:order_number>/", views.confirmation, name="confirmation"),
    path("<str:order_number>/cancel/", views.cancel_order, name="cancel_order"),
]
