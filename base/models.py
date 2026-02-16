from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .modelUtils import SoftDeleteModel
    
class User(AbstractUser, SoftDeleteModel):
    USER = 'user'
    AGENT = 'agent'
    ADMIN = 'admin'
    
    STATUS_CHOICES = [
        (USER, 'User'),
        (AGENT, 'Agent'),
        (ADMIN, 'Admin')
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=STATUS_CHOICES, default=USER)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return f"Username:{self.username} --Email: {self.email}"
    

class Ticket(SoftDeleteModel):
    PENDING = "pending"
    SOLVED = "solved"
    FAILED = "failed"

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SOLVED, 'Solved'),
        (FAILED, 'Failed')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default=PENDING, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="created_tickets")
    assigned_to = models.ForeignKey(User, null= True, blank= True, on_delete=models.SET_NULL,   related_name="assigned_tickets")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}----({self.created_at})"
    

class Notifications(SoftDeleteModel):
    NOTIFICATION_TYPES = [
        ('ticket_created', 'Ticket Created'),
        ('ticket_status_updated', 'Ticket Status Updated'),
    ]
    users = models.ManyToManyField(User, related_name="notifications")
    notification_type = models.CharField(max_length=40, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"




    
