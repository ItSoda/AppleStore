from django.db import models
from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=128, blank=True, null=True)
    quantity = models.PositiveBigIntegerField(default=0)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category.name} | {self.price}"

    def discount_price(self):
        return round(float(self.price) - float(self.price) * float((self.discount / 100)))


class Images(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    img = models.ImageField(upload_to='all_images')
    products_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'фотогрфия'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user} | Продукт {self.product}'

    def sum(self):
        return int(self.product.price * self.quantity)
    