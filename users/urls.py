from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (EmailVerificationView, RedPasswordResetConfirmView,
                    RedPasswordResetDoneView, RedPasswordResetView,
                    RegistrationCreateView, UserLoginView)

app_name = 'users'

urlpatterns = [
    path("registration/", RegistrationCreateView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationView.as_view(), name='email_verify'),
    path("password_reset/", RedPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", RedPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", RedPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("password_reset/complete/", RedPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

