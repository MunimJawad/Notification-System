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
    
    
