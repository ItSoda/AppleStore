from django.urls import path
from .views import Registration, UserLoginView
from django.contrib.auth.views import LogoutView


app_name = 'users'

urlpatterns = [
    path("registration/", Registration.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
