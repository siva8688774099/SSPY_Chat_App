from typing import Any

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import CustomUsersModel


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=12, required=True)

    class Meta:
        model = CustomUsersModel
        fields = ["username", "email", "mobile", "password1", "password2"]


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)

    class Meta:
        model = CustomUsersModel
        fields = ["username", "password"]


class CustomPasswordResetSentMailForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    class Meta:
        model = CustomUsersModel
        fields = ["email"]

    def send_mail(
        self,
        subject: str,
        email_template_name: str,
        context: dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = None,
    ) -> None:

        # Email subject *must not* contain newlines
        body = render_to_string(email_template_name, context)

        send_mail(subject, body, from_email, [to_email], html_message=body)


class CustomPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label="Confirm new password", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUsersModel
        fields = ["new_password1", "new_password2"]
