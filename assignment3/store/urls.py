from django.urls import path
from .views import KeyValueStoreView

urlpatterns = [
    path('store/<str:key>/', KeyValueStoreView.as_view(), name='kv-store'),
]
