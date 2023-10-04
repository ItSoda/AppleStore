from django.urls import path
from .views import OrderCreateView, yookassa_payment

app_name = 'orders'


urlpatterns = [
    path("create_order/", OrderCreateView.as_view(), name='order_create'),
    path("payment/", yookassa_payment, name='payment_url'),
]