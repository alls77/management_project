from django.urls import re_path

from .consumers import WorkerConsumer


websocket_urlpatterns = (
    re_path(r'ws/workers/$', WorkerConsumer),
)
