from django.shortcuts import render
from django.http import JsonResponse

def test(request):
    return JsonResponse("Hello world.!",safe=False)