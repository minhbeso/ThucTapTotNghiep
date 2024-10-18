from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(min_length=2, max_length=150, required=True)
    last_name = forms.CharField(min_length=2, max_length=150, required=True)
    username = forms.CharField(min_length=6, max_length=150, required=True)
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)


class UpdateUserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["avatar", "last_name", "first_name", "email"]
