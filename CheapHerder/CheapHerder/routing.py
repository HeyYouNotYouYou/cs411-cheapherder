from channels.routing import route
from .consumers import *

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<group_pk>[0-9]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<group_pk>[0-9]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<group_pk>[0-9]+)/$"),
]