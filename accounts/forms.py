from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

ROLE_CHOICES = [
    ("junior", "Junior"),
    ("senior", "Senior")
]


class SignUpForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Role"
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Passwords do not match.")

        return cleaned


class LoginForm(AuthenticationForm):

    username = forms.CharField(label="Username")


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["bio", "profile_pic"]