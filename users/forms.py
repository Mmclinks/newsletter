from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Форма создания пользователя
    """
    phone_number = forms.CharField(max_length=15, required=False, help_text="Help")
    usable_password = None

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "avatar",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit:
            raise forms.ValidationError("Wrong number")
        return phone_number


class UserProfileForm(forms.ModelForm):
    """
    Форма профиля пользователя
    """
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "country",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
