import json

from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Group as PGroup


# consumers that handle websocket connection/disconnection/receive channels


# dummy consumer for handling ws_messages
@channel_session_user_from_http
def ws_connect(message, group_pk):

    # authentication for websocket endpoint
    if message.user.is_anonymous():
        message.reply_channel.send({'accept': False})
        return

    message.reply_channel.send({'accept': True})
    group_object = PGroup.objects.get(pk=group_pk)
    Group("id-%s" % group_object.pk).add(message.reply_channel)


# dummy consumer for handling ws_messages
@channel_session_user
def ws_message(message, group_pk):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    Group("id-%s" % group_pk).send({
        "text": json.dumps({
            "text": message["text"],
            "username": message.user.username[0],
        }),
    })


# dummy consumer for handling ws_messages
@channel_session_user
def ws_disconnect(message, group_pk):
    Group("id-%s" % group_pk).discard(message.reply_channel)