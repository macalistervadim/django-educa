import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.id = self.scope["url_route"]["kwargs"]["course_id"]
        self.room_group_name = f"chat_{self.id}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, code: int | None) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(
        self,
        text_data: str | None = None,
        bytes_data: bytes | None = None,
    ) -> None:
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                },
            )

    def chat_message(self, event: dict[str, str]) -> None:
        self.send(text_data=json.dumps(event))
