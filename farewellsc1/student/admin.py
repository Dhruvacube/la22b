from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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

admin.site.register(Student ,StudentAdmin)
