from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import *


# Register your models here.
class TitlesAdmin(admin.ModelAdmin):
    search_fields = list_display = (
        'title_name', 'title_stu', 'total_vote', 'gender')
    list_filter = ('title_stu', 'gender')
    readonly_fields = ('slug',)
    list_per_page = 20

    fieldsets = (
        (_('Title'), {'fields': ('title_name', 'colour',)}),
        (_('Gender'), {'fields': ('gender',)}),
        (_('Class'), {'fields': ('title_stu',)}),
        (_('Description'), {'fields': ('desc', 'slug')}),
        (_('Total No of Votes'), {'fields': ('total_vote',)}),
    )

    # Female
    def change_female(self, request, queryset):
        updated = queryset.update(gender='f')
        self.message_user(request, ngettext(
            '%d title was successfully made only for females.',
            '%d titles were successfully made only for females.',
            updated,
        ) % updated, messages.SUCCESS)
    change_female.short_description = "Set Gender To Female"

    # Male
    def change_male(self, request, queryset):
        updated = queryset.update(gender='m')
        self.message_user(request, ngettext(
            '%d title was successfully made only for males.',
            '%d titles were successfully made only for males.',
            updated,
        ) % updated, messages.SUCCESS)
    change_male.short_description = "Set Gender To Male"

    # All
    def change_all(self, request, queryset):
        updated = queryset.update(gender='ALL')
        self.message_user(request, ngettext(
            '%d title was successfully made for all genders.',
            '%d titles were successfully made for all genders.',
            updated,
        ) % updated, messages.SUCCESS)
    change_all.short_description = "Set Gender To All"

    # CLASS
    # sc-1
    def change_sc_1(self, request, queryset):
        updated = queryset.update(title_stu='SC-1')
        self.message_user(request, ngettext(
            '%d title was set to SC-1.',
            '%d titles were set to SC-1.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_1.short_description = "Set class to SC-1"

    # sc-2
    def change_sc_2(self, request, queryset):
        updated = queryset.update(title_stu='SC-2')
        self.message_user(request, ngettext(
            '%d title was set to SC-2.',
            '%d titles were set to SC-2.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_2.short_description = "Set class to SC-2"

    # sc3
    def change_sc_3(self, request, queryset):
        updated = queryset.update(title_stu='SC-3')
        self.message_user(request, ngettext(
            '%d title was set to SC-3.',
            '%d titles were set to SC-3.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_3.short_description = "Set class to SC-3"

    # commerce
    def change_commerce(self, request, queryset):
        updated = queryset.update(title_stu='COMMERCE')
        self.message_user(request, ngettext(
            '%d title was set to COMMERCE.',
            '%d titles were set to COMMERCE.',
            updated,
        ) % updated, messages.SUCCESS)
    change_commerce.short_description = "Set class to COMMERCE"

    # arts
    def change_arts(self, request, queryset):
        updated = queryset.update(title_stu='ARTS')
        self.message_user(request, ngettext(
            '%d title was set to ARTS.',
            '%d titles were set to ARTS.',
            updated,
        ) % updated, messages.SUCCESS)
    change_arts.short_description = "Set class to ARTS"

    # all
    def change_all_class(self, request, queryset):
        updated = queryset.update(title_stu='ALL')
        self.message_user(request, ngettext(
            '%d title was successfully set for all classes.',
            '%d titles were successfully set for all classes.',
            updated,
        ) % updated, messages.SUCCESS)
    change_all_class.short_description = "Set class to ALL"

    actions = ['change_male', 'change_female', 'change_all', 'change_sc_1',
               'change_sc_2', 'change_sc_3', 'change_commerce', 'change_arts', 'change_all_class']


class ParticipantAdmin(admin.ModelAdmin):
    search_fields = list_display = list_filter = ('student', 'title_part')
    list_per_page = 20

    fieldsets = (
        (_('Student Details'), {'fields': ('student',)}),
        (_('Details of Titles Participated'), {'fields': ('title_part',)}),
        (_('Total No of Votes'), {'fields': ('stu_vote',)}),
    )


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Participants, ParticipantAdmin)
