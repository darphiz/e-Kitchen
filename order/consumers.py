import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from .models import Order
from .utils import generate_order_code


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'order_channel'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )    
        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self,text_data):
        order_json = json.loads(text_data)
        action = order_json['action']
        if action == 'take_order':
            data = await self.take_order(order_json) 
            data["action"] = 'new_order'
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_for_fulfil',
                    'message':data
                    
                    }
            )
    async def send_for_fulfil(self,event):
        data = json.dumps(event['message'])
        await self.send(
            text_data = data
            )
        

    @database_sync_to_async
    def take_order(self,order_json):
        details = order_json['details']
        sender = self.scope['user']
        order_instance =  Order(taken_by=sender, details=details,order_code = generate_order_code())
        order_instance.save()
        return_data =model_to_dict(order_instance)
        return return_data
        

