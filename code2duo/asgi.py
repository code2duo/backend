"""
ASGI config for code2duo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import path

# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "code2duo.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from authentication.middleware import FirebaseAuthenticationMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": FirebaseAuthenticationMiddlewareStack(
            URLRouter(
                [
                    # path("ws/canvas/<str:room_id>/", CanvasConsumer.as_asgi()),
                ]
            )
        ),
    }
)
