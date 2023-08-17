from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status',)
    fields = ('id', 'first_name', 'last_name', 'email', 'address', 'basket_history', 
            'status', 'created', 'initiator')
    readonly_fields = ('created', 'initiator')