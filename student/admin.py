from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import Student


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    search_fields = list_display = ('name', 'hidden','gender','class_stu') 
    list_filter = ('gender','class_stu','hidden') 
    readonly_fields = ('view_profile_picture','slug',)
    list_per_page = 20

    fieldsets = (
        (_('Name'),{'fields':('name',)}),
        (_('Profile Picture'),{'fields':('view_profile_picture','profile_pic',)}),
        (_('Class'),{'fields':('class_stu',)}),
        (_('Hidden'),{'fields':('hidden',)}),
        (_("Data"),{'fields':('slug','gender','note')}),
        (_('Title / Nickname given by Students'),{'fields':('data',)}),
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

    def make_hidden(self, request, queryset):
        updated = queryset.update(hidden=True)
        self.message_user(request, ngettext(
            '%d student was successfully made hidden.',
            '%d students were successfully made hidden.',
            updated,
        ) % updated, messages.WARNING)
    make_hidden.short_description = "Make Profile Hidden"

    def make_public(self, request, queryset):
        updated = queryset.update(hidden=False)
        self.message_user(request, ngettext(
            '%d student was successfully made public.',
            '%d students were successfully made public.',
            updated,
        ) % updated, messages.SUCCESS)
    make_public.short_description = "Make Profile Public"

    ####CLASS
    #sc-1
    def change_sc_1(self, request, queryset):
        updated = queryset.update(class_stu='SC-1')
        self.message_user(request, ngettext(
            '%d title was set to SC-1.',
            '%d titles were set to SC-1.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_1.short_description = "Set class to SC-1"

    #sc-2
    def change_sc_2(self, request, queryset):
        updated = queryset.update(class_stu='SC-2')
        self.message_user(request, ngettext(
            '%d title was set to SC-2.',
            '%d titles were set to SC-2.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_2.short_description = "Set class to SC-2"

    #sc3
    def change_sc_3(self, request, queryset):
        updated = queryset.update(class_stu='SC-3')
        self.message_user(request, ngettext(
            '%d title was set to SC-3.',
            '%d titles were set to SC-3.',
            updated,
        ) % updated, messages.SUCCESS)
    change_sc_3.short_description = "Set class to SC-3"

    #commerce
    def change_commerce(self, request, queryset):
        updated = queryset.update(class_stu='COMMERCE')
        self.message_user(request, ngettext(
            '%d title was set to COMMERCE.',
            '%d titles were set to COMMERCE.',
            updated,
        ) % updated, messages.SUCCESS)
    change_commerce.short_description = "Set class to COMMERCE"

    #arts
    def change_arts(self, request, queryset):
        updated = queryset.update(class_stu='ARTS')
        self.message_user(request, ngettext(
            '%d title was set to ARTS.',
            '%d titles were set to ARTS.',
            updated,
        ) % updated, messages.SUCCESS)
    change_arts.short_description = "Set class to ARTS"

    actions = ['change_male','change_female', 'make_hidden', 'make_public', 'change_sc_1', 'change_sc_2', 'change_sc_3', 'change_commerce', 'change_arts', ]

admin.site.register(Student ,StudentAdmin)
