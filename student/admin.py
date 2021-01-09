from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import Student


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    search_fields = list_display = ('name', 'gender','class_stu') 
    list_filter = ('gender','class_stu') 
    readonly_fields = ('view_profile_picture','slug',)
    list_per_page = 20

    fieldsets = (
        (_('Name'),{'fields':('name',)}),
        (_('Profile Picture'),{'fields':('view_profile_picture','profile_pic',)}),
        (_('Class'),{'fields':('class_stu',)}),
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

admin.site.register(Student ,StudentAdmin)
