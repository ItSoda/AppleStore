from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (BasketModelViewSet, CategoryModelViewSet,
                       OrderModelViewSet, ProductModelViewSet,
                       ProductSearchView, UserModelViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)
router.register(r'categories', CategoryModelViewSet)
router.register(r'users', UserModelViewSet)
router.register(r'orders', OrderModelViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('auth/', views.obtain_auth_token),
    path('search/', ProductSearchView.as_view(), name='search-list'),
    # Вся регистрация в двух строчках
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
