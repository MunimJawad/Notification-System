from django.contrib import admin
from .models import User, Ticket, Notifications, Audit

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','status','created_by','assigned_to', 'created_at')
    list_filter = ('status', 'assigned_to', 'created_at')
    search_fields = ('title', 'created_by__username','assigned_to__username','status')
    autocomplete_fields = ['created_by','assigned_to']


admin.site.register(Notifications)
admin.site.register(Audit)