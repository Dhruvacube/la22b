from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import *

# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def home(request):
    return render(
        request,
        'cover.html',
        {
        'cover_body': Settings.objects.values('about_entry').get()['about_entry'], 
        }
    )
