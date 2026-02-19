from django.core.cache import cache
from ..models import Ticket
from ..serializers import TicketSerializer
from django.conf import settings
import logging

logger = logging.getLogger('base')

class TicketService:
    @staticmethod
    def get_tickets_for_user(user):
        
        cache_key = f"ticket_list_user_{user.id}"
        data = cache.get(cache_key) 

        if not data:
            logger.info(f"Fetching tickets from the database for user {user.id}")
            if user.role == "admin":
               tickets = Ticket.objects.select_related('created_by', 'assigned_to').all()
            else:
                tickets = Ticket.objects.select_related('created_by', 'assigned_to').filter(created_by=request.user)        

            serializer = TicketSerializer(tickets, many=True)

            data = serializer.data
            cache.set(cache_key, data, timeout=120)
        else:
            logger.info(f"Ticket data fetched from cache for user {user.id}: {data}") 
        return data