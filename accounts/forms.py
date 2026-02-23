from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=20, help_text="Enter a valid contact number.")
    accept_terms = forms.BooleanField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            profile = user.profile  # created via signal
            profile.phone = self.cleaned_data.get("phone")
            profile.save()
        return user
