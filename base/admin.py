from django.contrib import admin
from .models import User, Ticket, Notifications, Audit

# Register your models here.

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Notifications)
admin.site.register(Audit)