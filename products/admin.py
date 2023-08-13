from django.contrib import admin

from products.models import Images, Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Images)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'discount', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'discount', 'image', 'category')
    search_fields = ('name', )
    ordering = ('name', )
