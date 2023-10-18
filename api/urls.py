from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (BasketModelViewSet, CategoryModelViewSet,
                       OrderModelViewSet, ProductModelViewSet,
                       ProductSearchView, EmailVerificationAndUserUpdateView,
                       OrderCreateView, YookassaWebhookView,
                       ImageModelViewSet,)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'images', ImageModelViewSet)
router.register(r'baskets', BasketModelViewSet)
router.register(r'categories', CategoryModelViewSet)
router.register(r'orders', OrderModelViewSet)




urlpatterns = [
    path("", include(router.urls)),
    path('search/', ProductSearchView.as_view(), name='search-list'),
    # Вся регистрация в двух строчках
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationAndUserUpdateView.as_view(), name='email_verify'),
    path("update-user/", EmailVerificationAndUserUpdateView.as_view(), name='user-update'),
    path("order/create/", OrderCreateView.as_view(), name='order_create'),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name='yookassa_webhook'),
]
