from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User
from django.conf import settings

class Registration(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy("users:login")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'



