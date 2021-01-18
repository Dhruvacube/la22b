import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from gdstorage.storage import GoogleDriveStorage

if settings.PRODUCTION_SERVER or settings.DUMMY_PRODUCTION:
    fs = GoogleDriveStorage()
else:
    fs = FileSystemStorage()

# Create your models here.
def path_and_rename(instance, filename):
    from uuid import uuid4

    upload_to = 'profile_pic'
    ext = filename.split('.')[-1]
    
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os.path.join(upload_to, filename)

class Student(models.Model):
    name = models.CharField(max_length=250,verbose_name=_('Name of the Student'),unique=True)
    slug = models.CharField(max_length=250,verbose_name=_('Slug of the Student'),unique=True, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=path_and_rename, storage=fs)
    
    class_stu = models.CharField(
        max_length=10, 
        choices=(
            ('SC-1','SC-1'),
            ('SC-2', 'SC-2'),
            ('SC-3','SC-3'),
            ('COMMERCE','COMMERCE'),
            ('ARTS','ARTS'),
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
    hidden = models.BooleanField(default=False)
    data = models.TextField(verbose_name=_('Title given by the others'),default=dict)

    class Meta:
        ordering = ('class_stu', 'name')

    def __str__(self):
        return self.name
    
    def view_profile_picture(self):
        height = '100%'
        width = '70%'
        if self.profile_pic:
            return mark_safe(f'<img src="{self.profile_pic.url}" width="{width}" height={height}" style="border-radius: 10px;" />')
        else:
            return mark_safe(f'<img src="{settings.STATIC_URL}img/user_unknown.jpg" width="{width}" height="{height}" style="border-radius: 10px;"  />')
    
    def save(self, *args, **kwargs):
        import string
        self.nameb = ''
        for i in self.name.split(' '): self.nameb += str(i.capitalize()) + ' '
        self.name = self.nameb
        self.slug = '-'.join(self.name.lower().translate({ord(c): None for c in string.whitespace}))
        self.profile_pic = self.process_image_profile(self.profile_pic)
        return super(Student, self).save(*args, **kwargs)

    def process_image_profile(self, profile_pic):
        from PIL import Image, ImageFilter
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile
        import sys

        im = Image.open(profile_pic)
        outputIoStream = BytesIO()
        h1,w1 = im.size

        if h1 == 3072 or w1 == 2048:
            return profile_pic
        elif h1 > 3072 or w1 > 2048:
            im.resize((3072,2048), Image.ANTIALIAS)
            im.save(outputIoStream, format='JPEG')
        else:
            gaussImage = im.filter(ImageFilter.GaussianBlur(30))
            resized_im = gaussImage.resize((3072,2048), Image.ANTIALIAS)

            bg_w, bg_h = resized_im.size
            img_w, img_h = im.size
            offset = ((bg_w - img_w*3) // 2, (bg_h - img_h*3) // 2)
            resized_im.paste(im.resize((img_w*3, img_h*3), Image.ANTIALIAS), offset)
            resized_im.save(outputIoStream, format='JPEG')
        
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % profile_pic.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage  
    
    def delete(self, using=None, keep_parents=False):
        fs.delete(str(self.profile_pic))
        return super().delete(using=using, keep_parents=keep_parents)
