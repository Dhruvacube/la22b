from django.db import models
from student.models import Student
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Titles(models.Model):
    title_name = models.CharField(_('Title Name'),max_length=250,unique=True,null=True,blank=True)
    desc = models.TextField(_('Description of the Title'),blank=True,null=True)
    gender = models.CharField(
        max_length=6, 
        choices=(
            ('ALL','ALL'),
            ('m','Male'),
            ('f', 'Female'),
        ), 
        default='m',
        verbose_name=_('Gender')
    )
    title_stu = models.CharField(
        max_length=10, 
        choices=(
            ('ALL','ALL'),
            ('SC-1','SC-1'),
            ('SC-2', 'SC-2'),
            ('SC-3','SC-3'),
            ('COMMERCE','COMMERCE'),
            ('ARTS','ARTS'),
        ), 
        default='sc1',
        verbose_name=_('Class')
    )
    slug = models.CharField(max_length=250,verbose_name=_('Slug of the Title'),unique=True, blank=True, null=True)
    total_vote = models.PositiveBigIntegerField(_('Total No of Vote Registered'),default=0)

    def __str__(self):
        return self.title_name
    
    def save(self, *args, **kwargs):
        import string
        self.nameb = ''
        for i in self.title_name.split(' '): self.nameb += str(i.capitalize()) + ' '
        self.title_name = self.nameb
        
        slug1 = ''.join(self.title_name.lower().translate({ord(c): None for c in string.whitespace}))
        unwanted_char = ['.',"'",'"','>','<','?',"\\",'/','*','.',',','!','@','#','$','%','^','&','(',')','-','_','+','=','{','}','[',']','|',':',';',' ']
        self.slug = ''.join((filter(lambda i: i not in unwanted_char, slug1)))

        return super(Titles, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Titles"
        ordering = ('-total_vote', 'title_name')

class Participants(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_('Student Model'))
    title_part = models.ForeignKey(Titles, on_delete=models.CASCADE, verbose_name=_('Titles Model'))
    stu_vote = models.PositiveBigIntegerField(_('Total No of Vote Registered by this student for the event'),default=0)

    def __str__(self):
        return self.student.name
    
    class Meta:
        verbose_name_plural = "Participants"
        ordering = ('-stu_vote', 'title_part')
