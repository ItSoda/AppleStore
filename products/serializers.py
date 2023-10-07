from rest_framework import serializers, fields
from .models import Product, ProductCategory, Basket


class ProductSerializer(serializers.ModelSerializer):
    # Поле category расписывается не как цифра, а как целый обьект
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset = ProductCategory.objects.all(),
        many=True, # ЕСЛИ MtM
    )
    class Meta:
        model = Product
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name", "description", "image", )


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # Методы корзины 
    sum = fields.FloatField(required=False) # required  отвечает за то что это поле обязательное
    total_sum = fields.SerializerMethodField()
    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_sum', 'created_timestamp')
        read_only_fields = ('created_timestamp', )

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()