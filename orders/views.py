from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from common.views import TitleMixin
from .forms import OrderForm
import stripe
from http import HTTPStatus
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from products.models import Basket
stripe.api_key = settings.STRIPE_SECRET_KEY
from .models import Order


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/create_order.html'
    title = 'AppleRedStore - Order'
    form_class = OrderForm
    success_url = reverse_lazy('products:catalog')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('products:catalog')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('products:basket')) 
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )

        line_items = session
        # Fulfill the purchase...
        fulfill_order(line_items)
        # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(line_items):
    order_id = int(line_items.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payments()