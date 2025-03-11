import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        if "user" not in self.scope:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": "User not authenticated",
                    },
                ),
            )
            await self.close()
            return

        self.user = self.scope["user"]
        self.id = self.scope["url_route"]["kwargs"]["course_id"]
        self.room_group_name = f"chat_{self.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code: int | None) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(
        self,
        text_data: str | None = None,
        bytes_data: bytes | None = None,
    ) -> None:
        if text_data:
            try:
                text_data_json = json.loads(text_data)

                if "message" not in text_data_json:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "error": "Missing 'message' field",
                            },
                        ),
                    )
                    return

                message = text_data_json["message"]
                now = timezone.now()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "user": self.user.username,
                        "datetime": now.isoformat(),
                    },
                )
            except json.JSONDecodeError:
                await self.send(
                    text_data=json.dumps(
                        {
                            "error": "Invalid JSON",
                        },
                    ),
                )
            except Exception as e:
                await self.send(
                    text_data=json.dumps(
                        {
                            "error": str(e),
                        },
                    ),
                )

    async def chat_message(self, event: dict[str, str]) -> None:
        await self.send(text_data=json.dumps(event))
