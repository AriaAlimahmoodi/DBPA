from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'military_experience', 'nationality', 'height_cm', 'weight_kg', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    # در صورت نیاز می‌توان فرم ورود را هم سفارشی کرد
    pass
