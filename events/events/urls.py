"""
URL configuration for events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from meetings import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from channels.generic.websocket import AsyncWebsocketConsumer

schema_view = get_schema_view(
    openapi.Info(
        title="Events API",
        default_version="v0.0.7",
        description="A sample API for EventsKGU",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="d.glazow2016@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('meeting-api/v1/auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # path('meeting-api/v1/auth/', include('authentication.urls')),

    # path('api-authlogout/', views.logout_view),  # затычка
    # path('accounts/profile/', views.accounts_profile_redirect),  # затычка

    path('api-auth', include('rest_framework.urls')),

    path('meeting-api/v1/', include('meetings.urls')),
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
]

websocket_urlpatterns = [
    path('ws/', views.ChatWebSocket.as_asgi()),
]
