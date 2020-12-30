from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
