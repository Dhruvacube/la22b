from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from student.models import Student
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from datetime import timedelta


# Create your models here.
class Settings(models.Model):
    about_entry = models.TextField(
        _('The about us on the entry page'), null=True, blank=True)
    title_limit = models.IntegerField(
        _('No of times a one a vote for a particular title  per day'), default=5)
    nickname_limit = models.IntegerField(
        _('No of times a one a give nicknames per day'), default=20)
    confession_limit = models.IntegerField(
        _('No of times a one make a confessions day'), default=2)

    vote_nicknameassigntime_start = models.DateTimeField(
        _('Start Time limit of assigning votes and nickname'), default=timezone.now)
    vote_nicknameassigntime = models.DateTimeField(
        _('End Time limit of assigning votes and nickname'), default=timezone.now)

    def __str__(self):
        return 'Settings'

    class Meta:
        verbose_name_plural = "Settings"


class Confession(models.Model):
    date = models.DateTimeField(
        _('Date when this confession was added!'), default=timezone.now)
    confession = models.TextField(_('Confession'))

    def __str__(self):
        return 'Confession ' + str(self.id) + ' ' + str(self.date)


def validate_insta_id(insta_id):
    import string
    import requests
    response = requests.get("https://instagram.com/" + insta_id + "/")
    if response.status_code == 404:
        if insta_id == string.whitespace:
            raise ValidationError(
                _('please do not keep Instagram ID blank'),
            )
        raise ValidationError(
            _('%(value)s is not a instagram id'),
            params={'value': insta_id},
        )


class Contact(models.Model):
    name = models.ForeignKey(Student, limit_choices_to=models.Q(
        hidden=False), on_delete=models.DO_NOTHING)
    instagram_id = models.CharField(
        max_length=254, null=True, blank=True, validators=[validate_insta_id])

    email = models.EmailField(max_length=254, null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    resolved = models.BooleanField(default=False)
    date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.subject

    def instagram_id_url(self):
        return mark_safe(f'<a href="https://instagram.com/{self.instagram_id}/" target="_blank" rel="noopener noreferrer"><input type="button" class="default" value="Click Here"/></a>') if self.instagram_id else 'No Instagram Id provided'


class RemoveName(models.Model):
    student_models = models.OneToOneField(Student, limit_choices_to=models.Q(
        hidden=False), on_delete=models.DO_NOTHING, unique=True)
    time_field = models.DateTimeField(
        verbose_name=_('Time'), default=timezone.now)

    def __str__(self):
        return self.student_models.name

    class Meta:
        verbose_name_plural = 'Remove Name'
        ordering = ('-time_field',)
