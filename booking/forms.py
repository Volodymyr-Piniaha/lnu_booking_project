# booking/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Вказуємо поля, які користувач заповнює при реєстрації
        fields = ('username', 'email')