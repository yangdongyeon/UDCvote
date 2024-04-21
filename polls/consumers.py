from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'

        # Join chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Retrieve the username from the user object in the scope
        username = self.scope['user'].username
        await self.save_message(username, message)

        # Send message to chat group including the username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username  # Include username in the message sent to the group
            }
        )

    # Receive message from chat group
    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', 'Unknown')  # Default to 'Unknown' if username isn't included

        # Send message to WebSocket including the username
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Send the username along with the message
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        # Assuming ChatMessage model exists and has user and message fields
        from .models import ChatMessage, User
        # Retrieve the user by username
        user = User.objects.get(username=username)
        # Create the chat message
        ChatMessage.objects.create(user=user, message=message)

