from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


def register(request):
	if request.user.is_authenticated:
		messages.info(request, "You are already registered.")
		return redirect("home")

	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Welcome to ShirtVerse! Your account is ready.")
			return redirect("home")
	else:
		form = UserRegistrationForm()

	return render(request, "accounts/register.html", {"form": form})

# Create your views here.
