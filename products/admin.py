from django.contrib import admin

from products.models import Images, Product, ProductCategory, Basket

admin.site.register(ProductCategory)
admin.site.register(Images)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'description', 'price', 'quantity', 'discount', 'category')
    fields = ('name', 'color', 'description', ('price', 'quantity'), 'discount', 'image', 'category')
    search_fields = ('name', )
    ordering = ('name', )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
