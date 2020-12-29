from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('results/',include('results.urls')),
    path('student/',include('student.urls')),
    path('titles/',include('titles.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
