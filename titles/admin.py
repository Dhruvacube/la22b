from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *

# Register your models here.
class TitlesAdmin(admin.ModelAdmin):
    search_fields = list_display = list_filter = ('title_name',) 
    readonly_fields = ('slug',)
    list_per_page = 20

    fieldsets = (
        (_('Title'),{'fields':('title_name',)}),
        (_('Gender'),{'fields':('gender',)}),
        (_('Description'),{'fields':('desc','slug')}),
        (_('Total No of Votes'),{'fields':('total_vote',)}),
    )

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
