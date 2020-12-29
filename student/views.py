from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from titles.models import *

from .models import *
from .templatetags import extras


# Create your views here.
def student(request, slug):
    import ast 

    student = get_object_or_404(Student,slug=slug)
    titles = Titles.objects.filter(gender=student.gender).all()

    return render(
        request,
        'student.html',
        {
            'student':student,
            'media':settings.MEDIA_URL,
            'titles':titles,
            'slug':slug,
            'data' : ast.literal_eval(student.data).get('titles'),
            'titles_404': False if titles.count() else True,
            'data_404': False if len(ast.literal_eval(student.data) if student.data else []) else True,
        }
    )

def addnicknames(request, slug):
    import ast

    if request.method=="POST":
        nickname_req = request.POST['nickname']
        nickname = formattedNickname(nickname_req)
        
        data_list = ast.literal_eval(Student.objects.filter(slug=slug).values('data').get()['data'])
        titles = data_list.get('titles')
        
        if titles:
            n=0
            for i in titles:
                for j in i:
                    if j == nickname:
                        vote = int(i[-1] + 1)
                        titles.remove(i)
                        titles.append([nickname, vote])
                        n+=1
            if n == 0: titles.append([nickname, 1])
        else: titles = [[nickname,1]]
        data_list.update({'titles': titles})

        Student.objects.filter(slug=slug).update(data=data_list)
    
    messages.success(request, "The Nickname has succesfully added!")
    return redirect(reverse('Student Profile',args=[slug]))

def formattedNickname(nickname):
    a=''
    for i in nickname.split(' '): a += i.capitalize() + ''
    return a.strip(' ')
