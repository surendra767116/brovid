from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user",)
        widgets = {
            "address_line1": forms.TextInput(attrs={"placeholder": "House / Street"}),
            "address_line2": forms.TextInput(attrs={"placeholder": "Apartment, Landmark (optional)"}),
        }
