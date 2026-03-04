from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Notifications, User
from .websocket import send_ticket_notification

@receiver(post_save, sender=Ticket, dispatch_uid="ticket_created_notification")
def ticket_created(sender, instance, created, **kwargs):
    if created:
        recepients = list(User.objects.filter(role="admin"))
        if instance.assigned_to:
            recepients.append(instance.assigned_to)
        recepients = list(set(recepients))  # unique users

        notification = Notifications.objects.create(
            notification_type='ticket_created',
            title=f"New Ticket Created: {instance.title}",
            ticket=instance
        )
        notification.users.add(*recepients)

        #for user in recepients:
            #send_ticket_notification(
            #    user_id=user.id,
            #    ticket_id=instance.id,
            #    message=f"New ticket created: {instance.title}"
            #)
        send_ticket_notification(
            
            ticket_id=instance.id,
             message=f"New ticket created: {instance.title}"
            )