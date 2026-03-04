from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

#def send_ticket_notification(user_id: int, ticket_id: int, message: str = None):
def send_ticket_notification(ticket_id: int, message: str = None):
    channel_layer = get_channel_layer()
    group_name = "user_1"  # OK for testing

    payload = {
        "type": "ticket_notification",
        "ticket_id": ticket_id,
        "message": message or f"You have a new ticket: {ticket_id}"  # fixed typo
    }

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": payload   # ✅ changed from "text" to "message"
        }
    )