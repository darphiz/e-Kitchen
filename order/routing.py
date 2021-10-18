from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/order/',consumers.OrderConsumer.as_asgi()),
]
