from django.urls import path, include
from api.views import ProductModelViewSet, ProductCategoryListAPIView, BasketModelViewSet
from rest_framework import routers
from rest_framework.authtoken import views


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("products/category-list/", ProductCategoryListAPIView.as_view(), name="product_category_list"),
    path('apple-store-auth/', views.obtain_auth_token)
]
