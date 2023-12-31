from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


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
    
    # Вся регистрация
    path(r'auth/', include('djoser.urls')),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationAndUserUpdateView.as_view(), name='email_verify'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("update-user/", EmailVerificationAndUserUpdateView.as_view(), name='update-user'),
    path("order/create/", OrderCreateView.as_view(), name='order_create'),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name='yookassa_webhook'),


]
