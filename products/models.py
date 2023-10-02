from django.conf import settings
from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='all_images', null=True, blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['id']

    def __str__(self):
        return self.name
    


class Product(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = models.TextField()
    gb = models.CharField(default=128, max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=128, blank=True, null=True)
    quantity = models.PositiveBigIntegerField(default=0)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    category = models.ManyToManyField(ProductCategory)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"Продукт: {self.name} {self.gb}| Категория: {self.category.all()[0]} | {self.price}"
    
    def discount_price(self):
        return round(float(self.price) - float(self.price) * float((self.discount / 100)))


class Images(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    img = models.ImageField(upload_to='all_images')
    products_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self) -> str:
        return self.title

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity for basket in self])

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user} | Продукт {self.product}'

    def sum(self):
        return int(self.product.price * self.quantity)
    
    def de_json(self):
        basket_item = {
            'name': self.product.name,
            'color': self.product.color,
            'gb': self.product.gb,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item