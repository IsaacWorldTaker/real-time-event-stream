from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from models import Event

class EventPublisher:
    @classmethod
    def publish(cls, *, channel: str, payload: dict):
        """
        Persists and event and fans it out to subscribers
        """
        with transaction.atomic():
            last=Event.objects.filter(channel=channel).order_by('-sequence_id').first()
            next_sequence_id=last.sequence_id+1 if last else 1

            event=Event.objects.create(channel=channel, sequence_id=next_sequence_id, payload=payload)
        cls._fan_out(event)
        return event
    @staticmethod
    def _fan_out(event):
        channel_layer=get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"events_{event.channel}",
            {
                "type": "event_message",
                "payload": {
                    "channel": event.channel,
                    "sequence": event.sequence_id,
                    "data": event.payload,
                }
            }
        )