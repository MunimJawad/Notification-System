from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "user_1"  # for testing
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("✅ CONNECT called")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("❌ DISCONNECTED", code)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['message']))
        print("📩 Sending message", event['message'])