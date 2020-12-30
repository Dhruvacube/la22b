import ast

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from titles.models import *

from .models import *
from .templatetags import extras

total_students = lambda: Student.objects.count()

# Create your views here.

#Student entry View
def entry(request):
    student_model = Student.objects.values('name','slug','profile_pic','class_stu').all()
    return render(
        request,
        'student-entry.html',
        {
            'total_students': total_students,
            'media': settings.MEDIA_URL,
            'student_model': student_model,
        }
    )

def search(request):
    query = request.GET['query']
    if len(query)>350:
        stu_list = Student.onjects.none()
        messages.warning(request, "Please limit your query to 350 characters or less only!")
    else:
        stuName = Student.objects.filter(name__icontains=query)
        stuClass = Student.objects.filter(class_stu__icontains=query)
        stutitle = Student.objects.filter(data__icontains=query)

        stu_list = stuName.union(stuClass,stutitle)
    return render(
        request,
        'student-entry.html',
        {
            'total_students': total_students,
            'media': settings.MEDIA_URL,
            'student_model': stu_list,
        }
    )

# Student Views
def student(request, slug):
    student = get_object_or_404(Student,slug=slug)
    titles = Titles.objects.filter(gender=student.gender).all()

    t1 = ast.literal_eval(student.data).get('titles')
    t = t1 if t1 else ['Dummy','List'] 

    return render(
        request,
        'student-profile.html',
        {
            'student':student,
            'media':settings.MEDIA_URL,
            'titles':titles,
            'slug':slug,
            'data' : sorted(t, key = lambda x: x[1], reverse=True),
            'titles_404': False if titles.count() else True,
            'data_404': False if len(ast.literal_eval(student.data) if student.data else []) else True,
            'total_students':total_students,
        }
    )

# Add nickname API
def addnicknames(request, slug):
    if request.method=="POST":
        nickname_req = request.POST['nickname']
        nickname = formattedNickname(nickname_req)
        if not nickname: 
            messages.error(request, "You entered only special characters which is not allowed!")
            return redirect(reverse('Student Profile',args=[slug]))
        
        data_list = ast.literal_eval(Student.objects.filter(slug=slug).values('data').get()['data'])
        titles = data_list.get('titles')
        
        if titles:
            n=0
            for i in titles:
                h=0
                for j in i:
                    if j == nickname:
                        print(j,i)
                        vote = int(i[-1] + 1)
                        print(vote)
                        titles.remove(i)
                        titles.append([nickname, vote])
                        n+=1
                        h+=1
                        break
                if h != 0: break
            if n == 0: titles.append([nickname, 1])
        else: titles = [[nickname,1]]
        data_list.update({'titles': titles})

        Student.objects.filter(slug=slug).update(data=data_list)
    
    messages.success(request, "The Nickname has succesfully added!")
    return redirect(reverse('Student Profile',args=[slug]))

# Returns a clean formatted nickname
def formattedNickname(nickname):
    import string
    unwanted_char = ['.',"'",'"','>','<','?',"\\",'/','*','.',',','!','@','#','$','%','^','&','(',')','-','_','+','=','{','}','[',']','|',':',';']
    nickname1 = ''.join((filter(lambda i: i not in unwanted_char, nickname)))
    a=''
    for i in nickname1.split(' '): a += i.capitalize() + ' '
    return a.strip(' ') if a != string.whitespace else False 
