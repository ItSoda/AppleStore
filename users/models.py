from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .managers import CustomUserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, )
    is_verified_email = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Переопределяем user`s manager 
    objects = CustomUserManager()

    def __str__(self):
        return f'Пользователь {self.email} | {self.first_name}'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
    
    def send_verification_email(self):
        link = reverse('api:email_verify', kwargs={'email': self.user.email, 'code': self.code})
        full_link = f'{settings.DOMAIN_NAME}{link}'
        subjects = f'Подтверждение учетной записи для {self.user.email}'
        message = 'Для подтверждения электронной почты {} перейдите по ссылке: {}.'.format(
            self.user.email,
            full_link,
        )
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
    