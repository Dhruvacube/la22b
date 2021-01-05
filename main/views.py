from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import *

def date_start_end():
    a = get_object_or_404(Settings)
    return True if a.vote_nicknameassigntime_start > timezone.now() or a.vote_nicknameassigntime < timezone.now() else False

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
