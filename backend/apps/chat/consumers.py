import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self) -> None:
        print("WebSocket connected")  # Вывод для отладки
        self.accept()

    def disconnect(self, code: int | None) -> None:
        print(f"WebSocket disconnected with code {code}")  # Вывод для отладки

    def receive(
        self,
        text_data: str | None = None,
        bytes_data: bytes | None = None,
    ) -> None:
        print(f"Received data: {text_data}")  # Вывод для отладки
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            self.send(text_data=json.dumps({"message": message}))
