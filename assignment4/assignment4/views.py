from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework import response
from rest_framework.throttling import UserRateThrottle
import logging

logger = logging.getLogger(__name__)

class AdminRateThrottle(UserRateThrottle):
    rate = '1000/minute' 

class RegularUserRateThrottle(UserRateThrottle):
    rate = '100/minute'
    
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    throttle_classes = [RegularUserRateThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return response({"message": "Hello, user!"})
    
from rest_framework.views import APIView

class AdminView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return response({"message": "Hello, admin!"})