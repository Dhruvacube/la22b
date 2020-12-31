from django.shortcuts import get_object_or_404, render

from .models import *


# Create your views here.
def title_entry(request):
    title_model = Titles.objects.values('title_name','slug','total_vote','desc').all()
    
    return render(
        request,
        'titles_entry.html',
        {
            'title_model':title_model,
        }
    )

def vote(request,slug):
    title_model = get_object_or_404(Titles,slug=slug)
    return render(
        request,
        'vote.html',
        {
            'title_model':title_model,
        }
    )
