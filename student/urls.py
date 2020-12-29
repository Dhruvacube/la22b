from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<slug:slug>', student, name="Student Profile"),
    path('addnickname/<slug:slug>', addnicknames, name="Add Nickname"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
