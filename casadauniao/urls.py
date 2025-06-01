# filepath: casadauniao/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render # Import render

# Define a simple view to render your index.html
def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('doadores.urls')), # Assuming your app urls are prefixed with api/
    path('', index_view, name='index'), # Serve index.html at the root
]