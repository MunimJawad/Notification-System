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