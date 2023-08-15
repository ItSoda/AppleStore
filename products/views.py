from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from common.views import TitleMixin

from .models import Images, Product, ProductCategory, Basket


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'AppleRedStore - Home'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    title = 'AppleRedStore - Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


class Search(ListView):
    model = Product
    template_name = 'products/catalog.html'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

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