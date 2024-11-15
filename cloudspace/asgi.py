"""
ASGI config for cloudspace project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from tokens.authentication import WebSocketJWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudspace.settings")

asgi_application = get_asgi_application()

from company.websockets import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            WebSocketJWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
