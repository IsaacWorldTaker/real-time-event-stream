from django.urls import re_path
from .consumers import EventConsumer

websocket_urlpatterns = [
    re_path(r"ws/events/(?P<channel>[\w\-]+)/$", EventConsumer.as_asgi()),
]
