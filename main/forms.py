from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import *


def date_start_end():
    a = get_object_or_404(Settings)
    return True if a.vote_nicknameassigntime_start > timezone.now() or a.vote_nicknameassigntime < timezone.now() else False


def date_start_end_else():
    a = get_object_or_404(Settings)
    return True if a.vote_nicknameassigntime < timezone.now() else False


class ConfessionForm(ModelForm):
    class Meta:
        model = Confession
        fields = ['confession', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['confession'].widget.attrs["class"] = "form-control"
        self.fields['confession'].widget.attrs["placeholder"] = "Type your confession ..."
        self.fields['confession'].widget.attrs["maxlength"] = "250"
        self.fields['confession'].widget.attrs["id"] = "confession_input"
        self.fields['confession'].widget.attrs["required"] = "true"
        self.fields['confession'].widget.attrs["rows"] = "1"
        self.fields['confession'].widget.attrs["disabled"] = date_start_end()


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'instagram_id', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs["class"] = "form-control form-select"
        self.fields['instagram_id'].widget.attrs["class"] = "form-control"
        self.fields['subject'].widget.attrs["class"] = "form-control"
        self.fields['message'].widget.attrs["class"] = "form-control"
        self.fields['email'].widget.attrs["class"] = "form-control"

        self.fields['instagram_id'].widget.attrs[
            "placeholder"] = "Instagram Username (Optional)"
        self.fields['email'].widget.attrs[
            "placeholder"] = "your_email_address@service-provider.com   (Optional)"
        self.fields['subject'].widget.attrs["placeholder"] = "Subject Heading"
        self.fields['message'].widget.attrs["placeholder"] = "Your Message ....."

        self.fields['name'].widget.attrs["disabled"] = date_start_end_else()
        self.fields['instagram_id'].widget.attrs["disabled"] = date_start_end_else()
        self.fields['subject'].widget.attrs["disabled"] = date_start_end_else()
        self.fields['message'].widget.attrs["disabled"] = date_start_end_else()
        self.fields['email'].widget.attrs["disabled"] = date_start_end_else()


class RemoveProfileForm(ModelForm):
    class Meta:
        model = RemoveName
        fields = ['student_models', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student_models'].widget.attrs["class"] = "form-control form-select"
        self.fields['student_models'].widget.attrs["style"] = "width:300px"
        self.fields['student_models'].widget.attrs["disabled"] = date_start_end_else()
