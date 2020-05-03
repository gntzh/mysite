from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

from libs.channels.auth import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
