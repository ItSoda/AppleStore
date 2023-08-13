from django.views.generic import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .models import Images, Product, ProductCategory


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
