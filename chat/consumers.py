import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_'+str(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message_data_in_json = json.loads(text_data)
        message_content = message_data_in_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'send_chatroom_message',
                'message':message_content
            }
        )

    async def send_chatroom_message(self, kwargs):
        message_content = kwargs['message']
        
        await self.send(text_data=json.dumps(
            {
                'message':message_content
            }
        ))

    pass