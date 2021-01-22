from django import template
from titles.models import Participants

register = template.Library()


@register.filter(name='win_vote')
def win_vote(title_id):
    max_vote = Participants.objects.filter(
        title_part=title_id).values('stu_vote')
    return max_vote[0]['stu_vote']
