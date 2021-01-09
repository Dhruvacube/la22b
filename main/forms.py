from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import *


def date_start_end():
    a = get_object_or_404(Settings)
    return True if a.vote_nicknameassigntime_start > timezone.now() or a.vote_nicknameassigntime < timezone.now() else False

class ConfessionForm(ModelForm):
    class Meta:
        model = Confession
        fields = ['confession',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['confession'].widget.attrs["class"] = "form-control"
        self.fields['confession'].widget.attrs["placeholder"] = "Type your confession ..."
        self.fields['confession'].widget.attrs["maxlength"] = "250"
        self.fields['confession'].widget.attrs["id"] = "confession_input"
        self.fields['confession'].widget.attrs["required"] = "true"
        self.fields['confession'].widget.attrs["rows"] = "1"
        self.fields['confession'].widget.attrs["disabled"] = date_start_end()
