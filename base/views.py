from django.shortcuts import render
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .utils import schema_for_method
from .import models
from django.core.cache import cache
import logging
from .services.ticket_service import TicketService
logger = logging.getLogger(__name__)

def test(request):
    return render(request, 'test.html')


@extend_schema_view(
    post=schema_for_method(summary="Create New User",description="Register new user here",request=serializers.CreateUserSerializer,responses=serializers.CreateUserSerializer,tags=["User Management"]),            
)
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data, context = {"request": request})

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "message": "User created Successfully",

            },status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema_view(
  get = schema_for_method(summary="Ticket List", description="Fetch ticket list based on permission", request=None, responses={200:serializers.TicketSerializer},tags=["Ticket Management"]),
  post = schema_for_method(summary="Create Ticket", description="Create Ticket", request=serializers.TicketSerializer, responses={200:serializers.TicketSerializer},tags=["Ticket Management"])
)
class TicketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"ticket_list_user_{request.user.id}"
        data = cache.get(cache_key)

        if not data:
            logger.info(f"Fetching tickets from DB for user {request.user.id}")
            tickets = TicketService.get_tickets_for_user(request.user)
            serializer = serializers.TicketSerializer(tickets, many=True, context={"request": request})
            data = serializer.data
            cache.set(cache_key, data, timeout=120)
        else:
            logger.info(f"Ticket data fetched from cache for user {request.user.id}")

        return Response(data, status=status.HTTP_200_OK)
        
    def post(self, request):        
        serializer = serializers.TicketSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        return Response(serializers.TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
      