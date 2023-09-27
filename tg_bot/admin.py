from django.contrib import admin
from .models import TG_USER



@admin.register(TG_USER)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'created_date')
    fields = ('user_id', 'first_name', 'last_name', 'username', 'created_date', 'update_date')
    readonly_fields = ('created_date', )