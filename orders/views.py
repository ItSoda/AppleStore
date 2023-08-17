from django.urls import reverse_lazy
from django.views.generic import CreateView
from common.views import TitleMixin
from .forms import OrderCreateForm

class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/create_order.html'
    title = 'AppleRedStore - Order'
    form_class = OrderCreateForm
    success_url = reverse_lazy('products:catalog')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)