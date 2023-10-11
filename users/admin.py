from django.contrib import admin

from products.admin import BasketAdmin

from .models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    inlines = (BasketAdmin, )

@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'expiration')