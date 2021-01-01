import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from gdstorage.storage import GoogleDriveStorage

if settings.PRODUCTION_SERVER:
    fs = GoogleDriveStorage()
else:
    fs = FileSystemStorage()

# Create your models here.
def path_and_rename(instance, filename):
    from uuid import uuid4
    upload_to = 'profile_pic'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
    return os.path.join(upload_to, filename)

class Student(models.Model):
    name = models.CharField(max_length=250,verbose_name=_('Name of the Student'),unique=True)
    slug = models.CharField(max_length=250,verbose_name=_('Slug of the Student'),unique=True, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=path_and_rename, storage=fs)
    
    class_stu = models.CharField(
        max_length=6, 
        choices=(
            ('sc1','SC-1'),
            ('sc2', 'SC-2'),
            ('sc3','SC-3'),
            ('com','COMMERCE'),
            ('arts','ARTS'),
        ), 
        default='sc1',
        verbose_name=_('Class')
    )
    gender = models.CharField(
        max_length=6, 
        choices=(
            ('m','Male'),
            ('f', 'Female'),
        ), 
        default='m',
        verbose_name=_('Gender')
    )
    note = models.TextField(blank=True,null=True)
    data = models.TextField(verbose_name=_('Title given by the others'),default=dict)

    def __str__(self):
        return self.name
    
    def view_profile_picture(self):
        height = width = '40%'
        if self.profile_pic:
            return mark_safe(f'<img src="{settings.MEDIA_URL}{self.profile_pic}" width="{width}" height={height}" style="border-radius: 10px;" />')
        else:
            return mark_safe(f'<img src="{settings.STATIC_URL}img/user_unknown.jpg" width="{width}" height="{height}" style="border-radius: 10px;"  />')
    
    def save(self, *args, **kwargs):
        import string
        self.nameb = ''
        for i in self.name.split(' '): self.nameb += str(i.capitalize()) + ' '
        self.name = self.nameb
        self.slug = '-'.join(self.name.lower().translate({ord(c): None for c in string.whitespace}))
        return super(Student, self).save(*args, **kwargs)
    
    def delete(self, using=None, keep_parents=False):
        fs.delete(str(self.profile_pic))
        return super().delete(using=using, keep_parents=keep_parents)
