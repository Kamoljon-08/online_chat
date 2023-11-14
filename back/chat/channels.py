from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'chat',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def chat_message(self, event):
        await self.send(text_data=event['message'])
        await self.send(text_data=f"{event['message']} (sent from server)")