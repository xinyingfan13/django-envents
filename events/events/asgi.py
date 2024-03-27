"""
ASGI config for events project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.sessions import CookieMiddleware, SessionMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddleware
from django.urls import path
from events import urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')

django_asgi_app = get_asgi_application()

'''application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": CookieMiddleware(SessionMiddleware(URLRouter(urls.websocket_urlpatterns))),
})'''
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddleware(
            URLRouter(urls.websocket_urlpatterns)
        )
    )
})

