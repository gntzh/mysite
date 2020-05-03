from time import time as now
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# FIXME 多进程下Python变量限制连接数量不可靠, 考虑使用Redis, 或者在Nginx处限制最大链接数
CHAT_USER_NUM = 0

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'chat'
        global CHAT_USER_NUM
        if CHAT_USER_NUM > 99:
            return
        if not self.scope['user'].is_active:
            return
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        CHAT_USER_NUM += 1

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        global CHAT_USER_NUM
        CHAT_USER_NUM -= 1

    async def receive_json(self, text_data_json):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': text_data_json['message'],
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
                'time': now(),
            }
        )

    async def chat_message(self, event):
        await self.send_json({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'time': event['time'],
        })
