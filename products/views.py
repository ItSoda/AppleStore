from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic.list import ListView

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
        context['categories_iphone'] = ProductCategory.objects.filter(name__startswith="iPhone ").order_by('id')
        context['categories_pods'] = ProductCategory.objects.filter(name__startswith="Apple AirPods ").order_by('id')
        context['categories_watch'] = ProductCategory.objects.filter(name__startswith="Apple Watch ").order_by('id')
        context['categories_ipad'] = ProductCategory.objects.filter(name__startswith="iPad ").order_by('id')
        context['categories_mac'] = ProductCategory.objects.filter(name__startswith="Mac").order_by('id') | ProductCategory.objects.filter(name__startswith="iMac ").order_by('id')
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
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

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
    product = Product.objects.get(id=product_id)
    images = Images.objects.filter(products_id=product)
    im1 = images.get(title='image_first')
    im2 = images.get(title='image_second')
    im3 = images.get(title='image_last')
    title = 'AppleRedStore'

    context = {
        'title': title,
        'products': product,
        'images': images,
        'im_list': [im1, im2, im3]
    }
    return render(request, 'products/product.html', context)