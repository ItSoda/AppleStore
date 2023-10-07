from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.db.models import Q
from django.core.cache import cache
from common.views import TitleMixin

from .models import Basket, Images, Product, ProductCategory


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    title = 'AppleRedStore - Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category=category_id) if category_id else queryset


class IndexListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    title = 'AppleRedStore - Home'

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        categories = cache.get('products_category')

        # Фильтрация категорий с использованием Q-объектов
        if categories is None:
            categories = ProductCategory.objects.filter(
                Q(name__startswith="iPhone") |
                Q(name__startswith="Apple AirPods") |
                Q(name__startswith="Apple Watch") |
                Q(name__startswith="iPad") |
                Q(name__startswith="Mac")
            )
            
            cache.set("products_category", categories, 10)
        # Создание словаря для категорий с разными ключами
        category_dict = {
            'iphone': [],
            'airpods': [],
            'watch': [],
            'ipad': [],
            'mac': [],
        }
        
        # Разделение категорий по ключам
        for category in categories:
            if category.name.startswith("iPhone"):
                category_dict['iphone'].append(category)
            elif category.name.startswith("Apple AirPods"):
                category_dict['airpods'].append(category)
            elif category.name.startswith("Apple Watch"):
                category_dict['watch'].append(category)
            elif category.name.startswith("iPad"):
                category_dict['ipad'].append(category)
            elif category.name.startswith("Mac"):
                category_dict['mac'].append(category)
            elif category.name.startswith("iMac"):
                category_dict['mac'].append(category)
        
        # Добавление словаря с категориями в контекст
        context['category_dict'] = category_dict
        return context


class Search(ListView):
    model = Product
    template_name = 'products/catalog.html'

    def get_queryset(self):
            search_query = self.request.GET.get('q', '')
            if ('[' or ']') not in search_query : # Допилить поиск чтобы все проходило
                return Product.objects.filter(name__iregex=search_query)
            else:
                return Product.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context



class BasketListView(TitleMixin, ListView):
    model = Basket
    title = 'AppleRedStore'
    template_name = 'products/basket.html'

    def get_context_data(self, **kwargs):
        context = super(BasketListView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id=product_id, user=request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_plus(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    basket = baskets.first()
    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_minus(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    basket = baskets.first()

    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def productView(request, product_id):
    title = 'AppleRedStore'
    product = Product.objects.get(id=product_id)
    images = Images.objects.filter(products_id=product)

    image_dict = {
        'first': {},
        'second': {},
        'last': {},
    }

    for image in images:
        if image.title.startswith('image_fir'):
            image_dict['first'] = image
        elif image.title.startswith('image_sec'):
            image_dict['second'] = image
        elif image.title.startswith('image_la'):
            image_dict['last'] = image

    context = {
        'title': title,
        'products': product,
        'images': images,
        'image_dict': image_dict
    }
    return render(request, 'products/product.html', context)