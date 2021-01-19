from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from main.models import *
from main.views import date_start_end, get_respect_date
from student.models import *
from student.views import total_students
from student.templatetags import extras

from .models import *

title_vote_limit = lambda: Settings.objects.values('title_limit').get_or_create()[0]['title_limit']

# Create your views here.
def title_entry(request):
    title_model = Titles.objects.values('title_name','slug','total_vote','desc','colour').all()
    
    return render(
        request,
        'titles_entry.html',
        {
            'title_model':title_model,
            'total_students': total_students,
        }
    )

def vote(request,slug):
    title_model = get_object_or_404(Titles,slug=slug)
    if title_model.title_stu == 'ALL' and title_model.gender == 'ALL':
        student_model = Student.objects.filter(hidden=False).values('name','slug','class_stu').all()
        class_model = Student.objects.filter(hidden=False).values('class_stu',).distinct('class_stu')
    
    elif title_model.title_stu == 'ALL':
        student_model = Student.objects.filter(hidden=False,gender=title_model.gender,).values('name','slug','class_stu').all()
        class_model = Student.objects.filter(hidden=False,gender=title_model.gender,).values('class_stu',).distinct('class_stu')

    elif title_model.gender == 'ALL':
        student_model = Student.objects.filter(hidden=False,class_stu=title_model.title_stu).values('name','slug','class_stu').all()
        class_model = Student.objects.filter(hidden=False,class_stu=title_model.title_stu).values('class_stu',).distinct('class_stu')

    else:
        student_model = Student.objects.filter(hidden=False,gender=title_model.gender,class_stu=title_model.title_stu).values('name','slug','class_stu')
        class_model = Student.objects.filter(hidden=False,gender=title_model.gender,class_stu=title_model.title_stu).values('class_stu',).distinct('class_stu')
    print(class_model)
    return render(
        request,
        'vote.html',
        {
            'title_model': title_model,
            'student_model': student_model,
            'slug': slug,
            'class_model':class_model,
            'profile_stu': True,
            'total_students': total_students,
            'participants_model_ten':Participants.objects.filter(title_part=title_model).order_by('-stu_vote').all()[:10],
            'date_start_end':date_start_end,
            'starts_end': get_respect_date()[1],
            'get_date': str(get_respect_date()[0].strftime("%b %d, %Y %X")),
        }
    )

#Api that will handel the vote counting
def register_vote(request):
    if request.method=="POST":
        student_slug = request.POST['student']
        title_slug = request.POST['title_name']

        student_model = Student.objects.filter(slug=student_slug).get()
        title_model = Titles.objects.filter(slug=title_slug).get()

        student_dict = f'{student_slug}-{title_slug}'

         #Update or create vote
        if request.session.get(student_dict, 0) > title_vote_limit():
            messages.error(request, "You have voted more than 5 times a day for a specific person!")
            return redirect(reverse('Vote Title', args=[title_slug]))
            
        elif request.session.get(student_dict) or request.session.get(student_dict,0) < title_vote_limit():
            try: request.session[student_dict] = request.session[student_dict] + 1
            except: request.session[student_dict] = 1
                
            if Participants.objects.filter(student=student_model, title_part=title_model).exists():
                Participants.objects.filter(
                    student=student_model, 
                    title_part=title_model,
                ).update(
                    stu_vote = F('stu_vote') + 1,
                )
            else:
                p = Participants(
                    student=student_model, 
                    title_part=title_model,
                    stu_vote = 1,
                )
                p.save()
            Titles.objects.filter(slug=title_slug).update(total_vote = F('total_vote') + 1)
                
            messages.success(request, "Vote succesfully registered!")
            return redirect(reverse('Success Redirect', args=[title_slug]))
    else:
         return redirect(reverse('View Title'))

def successredirect(request,slug):
    return render(request,
    'success/vote_success.html',
    {
        'redirect_link': reverse('Vote Title',args=[slug]),
    }
    )
