"""
URL configuration for Orion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import registro
from .chats import telegram, messenger, webChat, whatsapp

urlpatterns = [
    path('', registro.home, name='inicio'),
    path('whatsappRegister/', registro.registroWhatsapp),
    path('admin/', admin.site.urls),
    path('webhook/', whatsapp.whatsAppWebhook),
    path('login/',registro.login),
    path('autenticacion/', registro.autenticacion),
    path('confirmacion/',registro.confirmacion),
    path('telegram/',telegram.telegramConnetion),
    path('facebookMessenger/',messenger.messengerConnection),
    path('webchat/',webChat.chatweb),
    path('fwebhook/', messenger.messengerWebhook)
]
