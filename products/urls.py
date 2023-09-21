from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (BasketListView, IndexListView, ProductsListView, Search,
                    basket_add, basket_minus, basket_plus, basket_remove,
                    productView)

app_name = 'products'

urlpatterns = [
    path("catalog/", ProductsListView.as_view(), name='catalog'),
    path("category/<int:category_id>/", ProductsListView.as_view(), name='category'),
    path("search/", Search.as_view(), name='search'),
    path("basket/add/<int:product_id>/", basket_add, name='basket_add'),
    path("basket/list", login_required(BasketListView.as_view()), name='basket'),
    path("basket/plus/<int:product_id>/", basket_plus, name='basket_plus'),
    path("basket/minus/<int:product_id>/", basket_minus, name='basket_minus'),
    path("basket/remove/<int:basket_id>/", basket_remove, name='basket_remove'),
    path("product/<int:product_id>/", productView, name='product'),
]
