from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import Profile


def signup_view(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            messages.success(request, "Account created! Please log in.")

            return redirect("login")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return redirect("resource_list")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "junior"}
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Profile updated!")

            return redirect("edit_profile")

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
            "profile": profile,
            "role": profile.role   # ⭐ IMPORTANT FIX
        }
    )