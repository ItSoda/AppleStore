from django.urls import path
from .views import OrderCreateView, yookassa_payment, yookassa_webhook

app_name = 'orders'


urlpatterns = [
    path("create_order/", OrderCreateView.as_view(), name='order_create'),
    path("payment/", yookassa_payment, name='payment_url'),
    path("webhook/yookassa/", yookassa_webhook, name='webhook_yookassa'),
]