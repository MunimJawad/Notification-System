from django.core.cache import cache
from ..models import Ticket
from django.conf import settings
import logging

logger = logging.getLogger('base')

class TicketService:
    @staticmethod
    def get_tickets_for_user(user):
          if user.role == "admin":
              return Ticket.objects.select_related('created_by', 'assigned_to').all()
          return Ticket.objects.select_related('created_by', 'assigned_to').filter(created_by=user)
    
    @staticmethod
    def create_ticket(user, validated_data):
        assigned_to = validated_data.pop("assigned_to", None)

        ticket = Ticket.objects.create(
            assigned_to = assigned_to,
            created_by = user,
            **validated_data
        )

        cache.delete(f"ticket_list_user_{user.id}")

        return ticket