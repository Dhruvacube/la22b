from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Settings(models.Model):
    about_entry = models.TextField(_('The about us on the entry page'))
    title_limit = models.IntegerField(_('No of times a one a vote for a particular title  per day'), default = 5)
    nickname_limit = models.IntegerField(_('No of times a one a give nicknames per day'), default = 20)
    
    vote_nicknameassigntime_start = models.DateTimeField(_('Start Time limit of assigning votes and nickname'))
    vote_nicknameassigntime = models.DateTimeField(_('End Time limit of assigning votes and nickname'))

    def __str__(self):
        return 'Settings'

    class Meta:
        verbose_name_plural = "Settings"
