from django.contrib import admin

from products.models import Basket, Images, Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Images)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'description', 'price', 'quantity', 'discount',)
    fields = ('name', 'color', 'gb', 'description', ('price', 'quantity'), 'discount', 'images', 'category')
    search_fields = ('name', )
    ordering = ('name', )
    filter_horizontal = ['category', 'images']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
