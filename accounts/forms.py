from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        exists = get_user_model().objects.filter(email=email)
        if exists.count():
            raise ValidationError("email already exists")
        return email
