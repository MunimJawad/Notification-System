from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

class ActivityTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            self.track_user_activity(request)
        return response
    
    def track_user_activity(self,request):
        user = request.user

        last_activity_time = user.last_activity_time

        inactivity_limit = settings.JWT_EXPIRY_INACTIVITY_LIMIT

        if(now()-last_activity_time).seconds > inactivity_limit:
            raise PermissionDenied("Session expired due to inactivity.")
        else:
            user.update_last_activity_time()
            #self.refresh_access_token(request)

    def refresh_access_token(self,request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
"""
# middleware.py
import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from jwt import InvalidTokenError
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware  # ✅ correct import for Channels 4.x

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):

   # Custom WebSocket middleware for JWT Authentication in Channels 4.x.
 
    async def __call__(self, scope, receive, send):
        token = None
        query_string = scope.get("query_string", b"").decode()
        
        if "token=" in query_string:
            for param in query_string.split("&"):
                if param.startswith("token="):
                    token = param.split("token=")[1]
                    break

        if token:
            try:
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_data.get("user_id")
                scope["user"] = await self.get_user(user_id)
            except InvalidTokenError:
                scope["user"] = None
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)  """