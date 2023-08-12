from django.urls import path, include
from .views import ProductsListView, Search


app_name = 'products'

urlpatterns = [
    path("catalog/", ProductsListView.as_view(), name='catalog'),
    path("category/<int:category_id>/", ProductsListView.as_view(), name='category'),
    path("search/", Search.as_view(), name='search'),

]
