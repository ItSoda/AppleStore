from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title
