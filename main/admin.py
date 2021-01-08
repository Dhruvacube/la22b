from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _

from .models import *


# Register your models here.
class SettingsAdmin(admin.ModelAdmin):
    search_fields = list_display = ('about_entry','title_limit','nickname_limit','vote_nicknameassigntime_start','vote_nicknameassigntime')

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

class ConfessionAdmin(admin.ModelAdmin):
    search_fields = list_display = ('confession', 'date')
    list_filter = ('date',)
    list_per_page = 30
    fieldsets = (
        (_('Confession'),{'fields':('confession',)}),
        (_('Date'),{'fields':('date',)}),
    )


admin.site.register(LogEntry)
admin.site.register(Settings,SettingsAdmin)
admin.site.register(Confession,ConfessionAdmin)

admin.site.unregister(Group)

admin.site.site_header = 'Landmark of APS 2020'
admin.site.site_title = 'Landmark of APS 2020'
admin.site.index_title = 'Landmark of APS 2020 · LA22B'
