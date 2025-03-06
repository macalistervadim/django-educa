from typing import Any
from unittest.mock import patch

from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase

from backend.config.asgi import application


class TestChatConsumer(TestCase):
    async def asyncSetUp(self) -> None:
        self.user = await sync_to_async(get_user_model().objects.create_user)(
            username="testuser",
            password="testpassword",
        )

    @patch("channels.layers.get_channel_layer")
    async def test_group_send(self, mock_channel_layer: Any) -> None:
        mock_channel_layer = mock_channel_layer.return_value
        communicator = WebsocketCommunicator(application, "/ws/chat/room/1/")
        connected = await communicator.connect()
        self.assertTrue(connected)

        message = {"message": "Test message"}
        await communicator.send_json_to(message)

        mock_channel_layer.group_send.assert_called_with(
            "chat_1",
            {
                "type": "chat_message",
                "message": "Test message",
                "user": self.user.username,
                "datetime": mock_channel_layer.group_send.return_value[
                    "datetime"
                ],
            },
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["message"], "Test message")

        await communicator.disconnect()

    @patch("channels.layers.get_channel_layer")
    async def test_invalid_message_format(
        self,
        mock_channel_layer: Any,
    ) -> None:
        mock_channel_layer = mock_channel_layer.return_value
        communicator = WebsocketCommunicator(application, "/ws/chat/room/1/")
        connected = await communicator.connect()
        self.assertTrue(connected)

        invalid_message = {"wrong_field": "Test message"}
        await communicator.send_json_to(invalid_message)

        mock_channel_layer.group_send.assert_not_called()

        response = await communicator.receive_json_from()
        self.assertNotEqual(response.get("message", None), "Test message")

        await communicator.disconnect()

    @patch("channels.layers.get_channel_layer")
    async def test_different_course_id(self, mock_channel_layer: Any) -> None:
        mock_channel_layer = mock_channel_layer.return_value

        communicator_1 = WebsocketCommunicator(application, "/ws/chat/room/1/")
        connected_1 = await communicator_1.connect()
        self.assertTrue(connected_1)

        communicator_2 = WebsocketCommunicator(application, "/ws/chat/room/2/")
        connected_2 = await communicator_2.connect()
        self.assertTrue(connected_2)

        await communicator_1.send_json_to({"message": "Message to room 1"})
        response_1 = await communicator_1.receive_json_from()
        self.assertEqual(response_1["message"], "Message to room 1")

        await communicator_2.send_json_to({"message": "Message to room 2"})
        response_2 = await communicator_2.receive_json_from()
        self.assertEqual(response_2["message"], "Message to room 2")

        await communicator_1.disconnect()
        await communicator_2.disconnect()

    @patch("channels.layers.get_channel_layer")
    async def test_disconnect(self, mock_channel_layer: Any) -> None:
        communicator = WebsocketCommunicator(application, "/ws/chat/room/1/")
        connected = await communicator.connect()
        self.assertTrue(connected)

        mock_channel_layer.group_add.assert_called_with(
            "chat_1",
            communicator.scope["channel"],
        )

        await communicator.disconnect()

        mock_channel_layer.group_discard.assert_called_with(
            "chat_1",
            communicator.scope["channel"],
        )
