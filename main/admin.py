from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import *


# Register your models here.
class SettingsAdmin(admin.ModelAdmin):
    search_fields = list_display = ('about_entry', 'title_limit', 'nickname_limit',
                                    'confession_limit', 'vote_nicknameassigntime_start', 'vote_nicknameassigntime',)

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
        (_('Confession'), {'fields': ('confession',)}),
        (_('Date'), {'fields': ('date',)}),
    )


class ContactAdmin(admin.ModelAdmin):
    search_fields = list_display = (
        'name', 'resolved', 'date_time', 'instagram_id', 'email',)
    list_filter = ('date_time', 'resolved')
    list_per_page = 20
    readonly_fields = ('date_time', 'instagram_id_url')
    fieldsets = (
        (_('Submitted by User'), {
         'fields': ('name', 'instagram_id', 'email', 'subject', 'message')}),
        (_('Date'), {'fields': ('instagram_id_url',) + list_filter}),
    )

    def resolve(self, request, queryset):
        updated = queryset.update(resolved=True)
        self.message_user(request, ngettext(
            '%d query was resolved',
            '%d queries were resolved',
            updated,
        ) % updated, messages.SUCCESS)
    resolve.short_description = "Resolve"

    def unresolve(self, request, queryset):
        updated = queryset.update(resolved=False)
        self.message_user(request, ngettext(
            '%d query was unresolved',
            '%d queries were unresolved',
            updated,
        ) % updated, messages.WARNING)
    unresolve.short_description = "Unresolve"

    actions = [resolve, unresolve]

    def has_add_permission(self, request):
        return False


class RemoveNameAdmin(admin.ModelAdmin):
    search_fields = list_display = ('student_models', 'time_field')
    list_filter = ('time_field',)
    readonly_fields = ('time_field',)
    list_per_page = 10


admin.site.register(LogEntry)
admin.site.register(RemoveName, RemoveNameAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Confession, ConfessionAdmin)

admin.site.unregister(Group)

admin.site.site_header = 'Landmark of APS 2020'
admin.site.site_title = 'Landmark of APS 2020'
admin.site.index_title = 'Landmark of APS 2020 · LA22B'
