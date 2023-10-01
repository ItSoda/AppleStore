from django.conf import settings
from django.contrib.auth.views import (LoginView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserRegistrationForm, RedPasswordResetForm, RedSetPasswordForm
from .models import EmailVerification, User


class RegistrationCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy("users:login")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'AppleRedStore - EmailVerification'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        EmailVerifications = EmailVerification.objects.filter(code=code, user=user)
        if EmailVerifications.exists() and not EmailVerifications.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
        

class RedPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = RedPasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")
    # Идет отправка почты
    email_template_name = "users/password_reset_email.html"


class RedPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class RedPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = RedSetPasswordForm
    success_url = reverse_lazy('users:login')

# class RedPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'users/password_reset_complete.html'