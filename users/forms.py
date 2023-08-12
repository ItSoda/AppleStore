from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User

class UserLoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form_auth_style", 'placeholder': "Введите адрес электронной почты"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Введите имя", 'required': "True"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form_auth_style", 'placeholder': "Введите пароль"
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Введите имя", 'required': "True"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Введите адрес электронной почты", 'required': "True"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Введите пароль", 'required': "True"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Подтвердите пароль", 'required': "True"
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')