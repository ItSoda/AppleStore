from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, ProductCategory, Basket
from products.serializers import ProductSerializer, ProductCategorySerializer, BasketSerializer
from .permissions import IsAdminOrReadOnly

# ModelViewSet is consisting of GET POST PUT PATCH DELETE
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )


class ProductCategoryListAPIView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    # Переопределил queryset для одного юзера
    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)
    
    # Логика создания корзины
    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product'] # Берем данные из запроса
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product': 'There is no product with this ID'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(product_id=product_id, user=request.user)
            serializer = self.get_serializer(obj)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)