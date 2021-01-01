from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.urls import reverse
from django.contrib import messages

from .models import *
from student.models import * 


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
    student_model = Student.objects.filter(gender=title_model.gender).values('name','slug').all()
 
    return render(
        request,
        'vote.html',
        {
            'title_model': title_model,
            'student_model': student_model,
            'slug': slug,
            'profile_stu': True,
        }
    )

#Api that will handel the vote counting
def register_vote(request):
       if request.method=="POST":
            student_slug = request.POST['student']
            title_slug = request.POST['title_name']
            print(student_slug)

            student_model = Student.objects.filter(slug=student_slug).get()
            title_model = Titles.objects.filter(slug=title_slug).get()

            #Update or create vote
            if request.session.get(student_slug, 0) > 5:
                messages.error(request, "You have voted more than 5 times a day for a specific person!")
                return redirect(reverse('Vote Title', args=[title_slug]))
            
            elif request.session.get(student_slug) or request.session.get(student_slug,0) <= 5 :
                try: request.session[student_slug] = request.session[student_slug] + 1
                except: request.session[student_slug] = 1
                print(request.session[student_slug])
                
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
                title_model.update(total_vote = F('total_vote') + 1)
                
                messages.success(request, "Vote succesfully registered!")
                return redirect(reverse('Vote Title', args=[title_slug]))

