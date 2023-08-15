from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import EmailVerificationView, RegistrationCreateView, UserLoginView

app_name = 'users'

urlpatterns = [
    path("registration/", RegistrationCreateView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationView.as_view(), name='email_verify'),
]
