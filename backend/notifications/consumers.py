# filepath: backend/notifications/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user = self.scope["user"] # Descomente se a autenticação estiver configurada
        # if not self.user.is_authenticated:
        #     await self.close()
        #     return

        # self.room_group_name = f'user_{self.user.id}_notifications'
        self.room_group_name = 'general_notifications' # Ou um grupo específico

        # Entrar no grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado ao servidor de notificações!'
        }))


    async def disconnect(self, close_code):
        # Sair do grupo da sala
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receber mensagem do WebSocket (do frontend) - opcional
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     # Lógica para lidar com mensagens recebidas do frontend, se necessário

    # Receber mensagem do grupo da sala (do backend)
    async def send_notification(self, event):
        message = event['message']
        # Enviar mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))
