from django.contrib import admin

from products.admin import BasketAdmin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    inlines = (BasketAdmin, )
