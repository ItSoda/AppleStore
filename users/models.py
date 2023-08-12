from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_verified_email = models.BooleanField(default=False)

