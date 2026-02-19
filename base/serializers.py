from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .services.user_service import create_user_service
from . import models
User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all(), message="Email already exists")
    ])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Passwords do not match"})        
        return attrs
    
    def create(self, validated_data):

        validated_data.pop("password2")
        request = self.context["request"]
        
        return create_user_service(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data['password'],
            role=validated_data.get('role'),
            created_by=request.user
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class TicketSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only = True, source='created_by')
    assignee = UserSerializer(read_only = False, required= False, source = 'assigned_to')
    class Meta:
        model = models.Ticket
        fields = [
            'title', 'description', 'status', 'creator', 'assignee',
            'created_at', 'updated_at'
        ]