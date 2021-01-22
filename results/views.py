from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from student.views import total_students
from titles.models import *
from .templatetags import votes


# Create your views here.
def leaderboard(request):
    titles_model = Titles.objects.all()
    participants_model = Participants.objects.all()

    total_votal = Titles.objects.aggregate(Sum('total_vote'))[
        'total_vote__sum']
    if not total_votal:
        messages.info(
            request, 'No voting has been done till now. So why don\'t you vote ?')
        return redirect(reverse('View Title'))

    return render(
        request,
        'leaderboard.html',
        {
            'total_students': total_students,
            'total_vote': total_votal,
            'titles_model': titles_model,
            'participants_model': participants_model,
        }
    )


def leaderboardEach(request, slug):
    titles_model = get_object_or_404(Titles, slug=slug)
    participants_model = Participants.objects.filter(
        title_part=titles_model).all()

    return render(
        request,
        'leaderboard-each.html',
        {
            'total_students': total_students,
            'titles_model': titles_model,
            'participants_model': participants_model,
        }
    )
