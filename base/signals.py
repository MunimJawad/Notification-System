from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Notifications, User

@receiver(post_save, sender=Ticket)
def ticeket_created(sender, instance, created, **kwargs):
    if created:
        notification = Notifications.objects.create(
            notification_type = 'ticket_created',
            title = f"New Ticket Created: {instance.title}",
            ticket = instance
        )
        #add logics based on your requirements

        recepients = User.objects.filter(role = "admin")
        notification.users.add(instance.assigned_to)