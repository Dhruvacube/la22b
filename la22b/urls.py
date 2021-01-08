from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name="Cover Page"),
    path('anime-characters-are-you/', views.animeChar, name="Which Anime Character are you?"),
    path('anime-characters-are-you-result/', views.animeCharResult, name="Which Anime Character are you Results"),
    
    path('results/',include('results.urls')),
    path('student/',include('student.urls')),
    path('titles/',include('titles.urls')),
    path('results/',include('results.urls')),

    url(r'^logout/$', views.user_logout, name='signout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
