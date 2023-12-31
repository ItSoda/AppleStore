import json
import logging
import uuid
from http import HTTPStatus

import stripe
from django.conf import settings
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import HttpResponse, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationFactory

from common.views import TitleMixin
from products.models import Basket

from .forms import OrderForm
from .models import Order

logger = logging.getLogger(__name__)


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/create_order.html'
    title = 'AppleRedStore - Order'
    form_class = OrderForm
    success_url = reverse_lazy('orders:payment_url')
    
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        order = form.save()
        baskets = Basket.objects.filter(user=self.request.user)

        self.request.session['order_id'] = order.id
        self.request.session['order_products'] = [basket.product.name for basket in baskets]
        self.request.session['order_price'] = baskets.total_sum()

        return super(OrderCreateView, self).form_valid(form)


def yookassa_payment(request):
    # Получите необходимые параметры для создания платежа
    # Например, сумму платежа и описание
    order_id = request.session.get('order_id')
    order_products = request.session.get('order_products')
    order_price = request.session.get('order_price')

    # Настройте ключи доступа
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    # Создайте объект платежа
    payment = Payment.create({
        'amount': {
            'value': str(order_price),
            'currency': 'RUB',
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': reverse_lazy('index')
        },
        "capture": True,
        "save_payment_method": True,
        'description': f'Order #{order_id}',
        'metadata': {
            'order_id': order_id,
            'order_products': ', '.join(order_products),
            },
    })

    # Перенаправьте пользователя на страницу оплаты Юкассы
    return render(request, 'orders/yookassa_payment.html', {'payment_url': payment.confirmation.confirmation_url, 'order_price': order_price})


@csrf_exempt
def yookassa_webhook(request):
    event_json = json.loads(request.body.decode("utf-8"))

    try:
        logger.info(f'Responce: {event_json}')
        notification = WebhookNotificationFactory().create(event_json)
        logger.info('Webhook is create')
        # Получаем айди заказа из метаданных уведомления
        order_id = notification.object.metadata.get('order_id')
        order = Order.objects.get(id=order_id)
        # Проверяем статус платежа
        if notification.object.status == 'succeeded':
            logger.info('good')
            order.update_after_success_payments()
            # Обновляем статус заказа
        elif notification.object.status == 'canceled':
            logger.info('bad')
            order.update_after_canceled_payments()
            # Обновляем статус заказа
    except Exception as e:
        logger.info('Ошибка создания вебхука %s', str(e))
                # Обработка ошибок при разборе уведомления
    return HttpResponse(status=200)