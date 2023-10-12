import json
import logging
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationFactory

from django.conf import settings 

from orders.models import Order
from orders.serializers import OrderSerializer
from products.models import Basket, Product, ProductCategory
from products.serializers import (BasketSerializer, ProductCategorySerializer,
                                  ProductSerializer)
from users.models import User
from users.serializers import UserSerializer
from djoser.views import UserViewSet
from users.models import EmailVerification

from .permissions import IsAdminOrReadOnly


logger = logging.getLogger(__name__)

# ModelViewSet is consisting of GET POST PUT PATCH DELETE
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None


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


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class EmailVerificationView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super(EmailVerificationView, self).get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        EmailVerifications = EmailVerification.objects.filter(code=code, user=user)
        try:
            if EmailVerifications.exists() and not EmailVerifications.last().is_expired():
                user.is_verified_email = True
                user.save()
            return Response({'EmailVerification': user.is_verified_email})
        except Exception:
            return Response({'EmailVerification': 'EmailVerification is expired or not exists'})


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None

    def get_queryset(self):
        queryset =  super(OrderModelViewSet, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderCreateView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраните заказ
            order = serializer.save(initiator=request.user)
            # Здесь получите необходимые параметры для создания платежа
            # Например, сумму платежа и описание
            baskets = Basket.objects.filter(user=self.request.user)

            order_id = order.id
            order_products = [basket.product.name for basket in baskets]
            order_price = Basket.basketmanager.total_sum()

            # Настройте ключи доступа
            Configuration.account_id = settings.YOOKASSA_SHOP_ID
            Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

            # Создайте объект платежа
            payment = Payment.create({
                'amount': {
                    'value': str(order_price),
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': reverse('index'),
                },
                "capture": True,
                "save_payment_method": True,
                'description': f'Order #{order_id}',
                'metadata': {
                    'order_id': order_id,
                    'order_products': ', '.join(order_products),
                },
            })

            # Перенаправьте пользователя на страницу оплаты Юкассы
            return Response({'payment_url': payment.confirmation.confirmation_url, 'order_price': order_price})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YookassaWebhookView(APIView):
    def post(self, request):
        event_json = json.loads(request.body.decode("utf-8"))

        try:
            logger.info(f'Responce: {event_json}')
            notification = WebhookNotificationFactory().create(event_json)
            logger.info('Webhook is create')
            # Получаем айди заказа из метаданных уведомления
            order_id = notification.object.metadata.get('order_id')
            order = Order.objects.get(id=order_id)
            # Проверяем статус платежа
            if notification.object.status == 'succeeded':
                logger.info('good')
                order.update_after_success_payments()
                # Обновляем статус заказа
            elif notification.object.status == 'canceled':
                logger.info('bad')
                order.update_after_canceled_payments()
                # Обновляем статус заказа
        except Exception as e:
            logger.info('Ошибка создания вебхука %s', str(e))
                    # Обработка ошибок при разборе уведомления
        return HttpResponse(status=200)