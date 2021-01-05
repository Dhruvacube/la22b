from django.db.models import Sum
from django.shortcuts import render
from student.views import total_students
from titles.models import *


# Create your views here.
def leaderboard(request):
    titles_model = Titles.objects.all()
    participants_model = Participants.objects.all()

    return render(
        request, 
        'leaderboard.html',
        {
            'total_students':total_students,
            'total_vote': Titles.objects.aggregate(Sum('total_vote'))['total_vote__sum'],
            'titles_model': titles_model,
            'participants_model': participants_model,
        }
    )
