import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer

from events.auth import can_subscribe
from events.models import Event
class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        user=self.scope['user']

        if user is None or user.is_anonymous:
            await self.close(code=4001)
            return
        self.channel_name_param=self.scope['url_route']['kwargs']['channel']
        self.group_name=f'events_{self.channel_name_param}'
        if not can_subscribe(user, self.channel_name_param):
            await self.close(code=4003)
            return
        query_params=parse_qs(self.scope['query_string'].decode())
        last_sequence=query_params.get('last_sequence', [None])[0]

        if last_sequence is not None:
            missed = Event.objects.filter(sequence_id__gt=int(last_sequence)).order_by('sequence_id')
            
            for event in missed:
                await self.send(text_data=json.dumps(
                    {
                        'channel':event.channel,
                        'sequence':event.sequence_id,
                        'data':event.payload
                    }
                ))

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channell_name
        )
    async def receive(self, text_data):
        data=json.loads(text_data)
        await self.send(text_data=json.dumps({
            'status':'ok',
            'data':data
        }))
        
    async def event_message(self, event):
    
        await self.send(text_data=json.dumps(event['payload']))