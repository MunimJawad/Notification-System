from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
User = get_user_model()

def create_user_service(username, email, password, role, created_by):
    if created_by.role == "admin":           
           new_user_role = role   
           if new_user_role == "admin":
               user = User.objects.create_user(
                   username=username,
                   email=email,
                   password=password,
                   role = new_user_role,
                   is_staff = True,
                   is_superuser = True
               )
           else:
               user = User.objects.create_user(
                   username=username,
                   email=email,
                   password=password,
                   role = new_user_role,
                   is_staff = False,
                   is_superuser = False
               )
        
           return user
        
    else:
        raise PermissionDenied("Only admin users can create new users")