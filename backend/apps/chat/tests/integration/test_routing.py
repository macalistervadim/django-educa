from channels.testing import WebsocketCommunicator
from django.test import TestCase

from backend.config.asgi import application


class TestWebSocketRouting(TestCase):
    async def test_connection_valid_url(self) -> None:
        communicator = WebsocketCommunicator(application, "/ws/chat/room/1/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
