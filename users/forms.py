from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)

from users.models import User

from .tasks import send_email_verify


class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form_auth_style", 'placeholder': "Введите адрес электронной почты"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form_auth_style", 'placeholder': "Введите пароль"
    }))

    class Meta:
        model = User
        fields = ('username', 'password')



class UserRegistrationForm(UserCreationForm):
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
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verify.delay(user.id)
        return user
    
class RedPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'Почта'}),
    )
    

class RedSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder':'Введите пароль'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder':'Повторите пароль'}),
    )