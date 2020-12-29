from django.contrib import admin
from django.contrib.admin.models import LogEntry

# Register your models here.
admin.site.register(LogEntry)

admin.site.site_header = 'Landmark of APS 2020'
admin.site.site_title = 'Landmark of APS 2020'
admin.site.index_title = 'Landmark of APS 2020 · LA22B'
