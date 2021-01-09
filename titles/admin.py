from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import *


# Register your models here.
class TitlesAdmin(admin.ModelAdmin):
    search_fields = list_display = ('title_name','title_stu','total_vote','gender')
    list_filter = ('title_stu','gender') 
    readonly_fields = ('slug',)
    list_per_page = 20

    fieldsets = (
        (_('Title'),{'fields':('title_name',)}),
        (_('Gender'),{'fields':('gender',)}),
        (_('Class'),{'fields':('title_stu',)}),
        (_('Description'),{'fields':('desc','slug')}),
        (_('Total No of Votes'),{'fields':('total_vote',)}),
    )

    #Female
    def change_female(self, request, queryset):
        updated = queryset.update(gender='f')
        self.message_user(request, ngettext(
            '%d title was successfully made only for females.',
            '%d titles were successfully made only for females.',
            updated,
        ) % updated, messages.SUCCESS)
    change_female.short_description = "Set Gender To Female"

    #Male
    def change_male(self, request, queryset):
        updated = queryset.update(gender='m')
        self.message_user(request, ngettext(
            '%d title was successfully made only for males.',
            '%d titles were successfully made only for males.',
            updated,
        ) % updated, messages.SUCCESS)
    change_male.short_description = "Set Gender To Male"

    #All
    def change_all(self, request, queryset):
        updated = queryset.update(gender='ALL')
        self.message_user(request, ngettext(
            '%d title was successfully made for all genders.',
            '%d titles were successfully made for all genders.',
            updated,
        ) % updated, messages.SUCCESS)
    change_all.short_description = "Set Gender To All"

    actions = ['change_male','change_female', 'change_all']

class ParticipantAdmin(admin.ModelAdmin):
    search_fields = list_display = list_filter = ('student','title_part') 
    list_per_page = 20

    fieldsets = (
        (_('Student Details'),{'fields':('student',)}),
        (_('Details of Titles Participated'),{'fields':('title_part',)}),
        (_('Total No of Votes'),{'fields':('stu_vote',)}),
    )

admin.site.register(Titles ,TitlesAdmin)
admin.site.register(Participants ,ParticipantAdmin)
