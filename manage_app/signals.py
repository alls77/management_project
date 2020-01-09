from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Worker


@receiver(post_save, sender=Worker)
@receiver(post_delete, sender=Worker)
def workers_update(sender, **kwargs):
    channel_layer = get_channel_layer()
    group_name = 'workers'

    async_to_sync(channel_layer.group_send)(
        group_name, {
            'type': 'update',
            'update': True,
        }
    )
