from django.urls import path

from . import consumers

websocket_urlpatterns = [
   path("project/log-trail", consumers.CompanyProjectLoggerConsumer.as_asgi())
]