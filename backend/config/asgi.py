import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from backend.apps.chat import routing as chat_routing

settings_module = os.getenv(
    "DJANGO_SETTINGS_MODULE",
    "backend.config.settings.development",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(chat_routing.websocket_urlpatterns),
        ),
    },
)

#
# if settings.DEBUG:
#     from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
#
#     application = ProtocolTypeRouter(
#         {
#             "http": ASGIStaticFilesHandler(django_asgi_app),
#             "websocket": AuthMiddlewareStack(
#                 URLRouter(chat_routing.websocket_urlpatterns),
#             ),
#         },
#     )
