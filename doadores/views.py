from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def example_view(request):
    data = {
        "message": "Hello, this is an example view!"
    }
    return JsonResponse(data)