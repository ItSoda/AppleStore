from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # style form
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Иван",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Иванов",
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "AppleRedStore@gmail.com",
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Москва, Улица Большая Полянка, 22",
    }))
    # register fields 
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')

