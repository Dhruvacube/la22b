from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', title_entry, name="View Title"),
    path('vote/<slug:slug>', vote, name="Vote Title"),
    path('registervote/', register_vote,name="Register Vote"),
    path('successredirect/<slug:slug>', successredirect, name="Success Redirect")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
