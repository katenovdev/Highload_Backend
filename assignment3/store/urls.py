from django.urls import path
from .views import KeyValueStoreView
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import make_wsgi_app, Counter, Gauge

urlpatterns = [
    path('store/<str:key>/', KeyValueStoreView.as_view(), name='kv-store'),
    path('metrics/', csrf_exempt(make_wsgi_app())),
]