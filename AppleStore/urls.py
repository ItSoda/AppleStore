"""
URL configuration for AppleStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from orders.views import yookassa_webhook
from products.views import IndexListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexListView.as_view(), name='index'),
    path("api/v1/", include('api.urls', namespace='api')),
    path("products/", include('products.urls', namespace='products')),
    path("users/", include('users.urls', namespace='users')),
    path("orders/", include('orders.urls', namespace='orders')),
    path('accounts/', include("django.contrib.auth.urls")),
    path("webhook/yookassa/", yookassa_webhook, name='webhook_yookassa'),
]


if settings.DEBUG:
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
