import json
from email import message
from math import e
from pydoc import text
from turtle import pos
from urllib import request

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer


class TestConsumer(WebsocketConsumer):

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'notification_%s' % self.room_name
        self.room_name = "test_consumer"
        self.room_group_name = "group_test_consumer"
        print(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,  # group name to add
            self.channel_name,  # channel name to add in group-> it will create a group with this name
        )
        self.accept()
        self.send(
            text_data=json.dumps({"status": "You're connected! to Django Channels"})
        )

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        self.send(text_data=text_data)

    def notification_message(self, event):
        print("Notification message calling")
        message_details = event
        print(message_details)
        self.send(text_data=json.dumps({"message": message_details["message"]}))


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send_json({"status": "You're connected to the chat room!"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):

        if text_data:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": text_data}
            )

    async def chat_message(self, event):
        message_details = json.loads(event["message"])

        await self.send_json({"message": message_details})
