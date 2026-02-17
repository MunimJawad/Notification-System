from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from . import serializers

def test(request):
    return render(request, 'test.html')

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

