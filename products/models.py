import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='all_images', null=True, blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    gb = models.CharField(default=128, max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=128, blank=True, null=True)
    quantity = models.PositiveBigIntegerField(default=0)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ManyToManyField(ProductCategory)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"Продукт: {self.name} {self.gb}| Категория: {self.category.all()[0]} | {self.price}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        return super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
    
    def discount_price(self):
        return round(float(self.price) - float(self.price) * float((self.discount / 100)))

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="rub",
            )
        return stripe_product_price


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
    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items

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