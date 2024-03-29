from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import json
from myapi.models import GroupChannel
from myapi.serializers import GroupChannel_dataSerializer

@database_sync_to_async
def get_user(user_id):
    try:
        return Users.objects.get(id=user_id)
    except:
        return AnonymousUser()


@database_sync_to_async
def create_notification(receiver, typeof="task_created", status="unread"):
    notification_to_create = notifications.objects.create(
        user_revoker=receiver, type_of_notification=typeof)
    print('I am here to help')
    return (notification_to_create.user_revoker.username, notification_to_create.type_of_notification)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print(self.scope)
        await self.accept()
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "hello world"
        }))
        self.room_name = 'online_user'
        self.room_group_name = 'online_user'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "room made"
        }))

    async def websocket_receive(self, event):
        data_to_get = json.loads(event['text'])
        if "group" in data_to_get:
            if data_to_get['status'] == "join":
                # c = GroupChannel(groupname =data_to_get["group"],channelname = self.channel_name)
                # await database_sync_to_async(c.save())()
                await self.channel_layer.group_add(data_to_get["group"], self.channel_name)
                await self.send(json.dumps({
                    "type": "websocket.send",
                    "text": "join group :"+data_to_get["group"]
                }))
            elif data_to_get['status'] == "leave":
                await self.channel_layer.group_discard(data_to_get["group"], self.channel_name)
                await self.send(json.dumps({
                    "type": "websocket.send",
                    "text": "leave group :"+data_to_get["group"]
                }))
            elif data_to_get['status'] == "list":
                list_group = await self.channel_layer.groups(self.channel_name)
                await self.send(json.dumps({
                    "type": "websocket.send",
                    "text": "list group :"+list_group
                }))
    async def websocket_disconnect(self, event):
        print('disconnect', event)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(json.dumps({
            "type": "websocket.send",
            "data": event
        }))
        print('I am here')
        print(event)

    async def system_load(self, event):
        # Receive data from group
        await self.send(text_data=json.dumps(event['data']))

    async def logDHT11_collect(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def logDHT11_collect(self, event):
        await self.send(text_data=json.dumps({"target": event['target'], "data": event['data']}))

    async def led_notification(self, event):
        await self.send(text_data=json.dumps({"target": event['target'], "data": event['data']}))

    async def door_notification(self, event):
        await self.send(text_data=json.dumps({"target": event['target'], "data": event['data']}))

    async def bh1750_collect(self, event):
        await self.send(text_data=json.dumps({"target": event['target'], "data": event['data']}))

    async def gas_collect(self, event):
        await self.send(text_data=json.dumps({"target": event['target'], "data": event['data']}))