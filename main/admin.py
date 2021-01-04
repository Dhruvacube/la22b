from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *

# Register your models here.
class SettingsAdmin(admin.ModelAdmin):
    search_fields = list_display = ('about_entry','title_limit','nickname_limit','vote_nicknameassigntime')

    def has_add_permission(self, request):
        num_objects = Settings.objects.count()
        if num_objects >= 1:
            return False
        return super(SettingsAdmin, self).has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        num_objects = Settings.objects.count()
        if num_objects >= 1:
            return False
        return super(SettingsAdmin, self).has_delete_permission(request,  obj=obj)


admin.site.register(LogEntry)
admin.site.register(Settings,SettingsAdmin)

admin.site.site_header = 'Landmark of APS 2020'
admin.site.site_title = 'Landmark of APS 2020'
admin.site.index_title = 'Landmark of APS 2020 · LA22B'
