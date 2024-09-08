from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.apps import apps  # ChatMessage 모델을 동적으로 가져오기 위해 사용
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

        # Load the last 50 chat messages when a user connects
        messages = await self.get_chat_history()

        # 비동기 데이터베이스 접근 문제 해결을 위해 명시적으로 리스트로 변환
        messages = list(messages)

        # 로그로 데이터 확인
        if not messages:
            print("No messages found.")
        else:
            for message in messages:
                print(message)  # 각 메시지 출력

                # 데이터 유효성 검사
                if 'message' in message and 'user__username' in message and 'timestamp' in message:
                    await self.send(text_data=json.dumps({
                        'message': message['message'],
                        'username': message['user__username'],
                        'timestamp': str(message['timestamp'])
                    }))
                else:
                    print("Invalid message data format:", message)

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
        # 동적으로 ChatMessage 모델을 가져옴
        ChatMessage = apps.get_model('polls', 'ChatMessage')
        from django.contrib.auth.models import User
        # Retrieve the user by username
        user = User.objects.get(username=username)
        # Create the chat message
        ChatMessage.objects.create(user=user, message=message)

    @database_sync_to_async
    def get_chat_history(self):
        # 동적으로 ChatMessage 모델을 가져옴
        ChatMessage = apps.get_model('polls', 'ChatMessage')
        # Get the last 50 chat messages ordered by timestamp
        return ChatMessage.objects.order_by('-timestamp').values('user__username', 'message', 'timestamp')[:50]




