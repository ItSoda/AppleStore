from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order #{self.id} | {self.first_name} {self.last_name}'

    def update_after_payments(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        purchased_item = []
        total_price = 0.0

        for basket in baskets:
            purchased_item.append(basket.de_json())
            total_price += basket.sum()

        self.basket_history = {
            'purchased_item': purchased_item,
            'total_price': total_price,
        }
        baskets.delete()
        self.save()