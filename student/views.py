import ast

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from main.models import *
from titles.models import *

from .models import *
from .templatetags import extras

total_students = lambda: Student.objects.count()
students_vote_limit = lambda: Settings.objects.values('nickname_limit').get()['nickname_limit']

# Create your views here.

#Student entry View
def entry(request):
    student_model = Student.objects.all()
    return render(
        request,
        'student-entry.html',
        {
            'total_students': total_students,
            'student_model': student_model,
        }
    )

def search(request):
    if request.method == 'GET':
        query = formattedNickname(request.GET['query'])
        if len(query)>350:
            stu_list = Student.onjects.none()
            messages.warning(request, "Please limit your query to 350 characters or less only!")

        stuName = Student.objects.filter(name__icontains=query.strip(' '))
        stuClass = Student.objects.filter(class_stu__icontains=query.strip(' '))
        stutitle = Student.objects.filter(data__icontains=query.strip(' '))

        stu_list = stuName.union(stuClass,stutitle)
        return render(
            request,
            'student-entry.html',
            {
                'total_students': total_students,
                'student_model': stu_list,
            }
        )
    else:
        return redirect(reverse('Student Entry Page'))

# Student Views
def student(request, slug):
    student = get_object_or_404(Student,slug=slug)
    titles = Titles.objects.filter(gender=student.gender).all()
    titles_all = Titles.objects.filter(gender='ALL').all()

    t1 = ast.literal_eval(student.data).get('titles')
    t = t1 if t1 else ['Dummy','List'] 

    return render(
        request,
        'student-profile.html',
        {
            'student':student,
            'titles':titles.union(titles_all),
            'slug':slug,
            'data' : sorted(t, key = lambda x: x[1], reverse=True),
            'titles_404': False if titles.count() else True,
            'data_404': False if len(ast.literal_eval(student.data) if student.data else []) else True,
            'total_students':total_students,
            'profile_stu': True,
        }
    )

# Add nickname API
def addnicknames(request, slug):
    if request.method=="POST":
        nickname_req = request.POST['nickname']
        nickname = formattedNickname(nickname_req.strip(' '))
        if not nickname: 
            messages.error(request, "You entered only special characters which is not allowed!")
            return redirect(reverse('Student Profile',args=[slug]))
        
        if request.session.get(slug, 0) > students_vote_limit():
            messages.error(request, "You have voted more than 5 times a day for a specific person!")
            return redirect(reverse('Student Profile',args=[slug]))
        
        elif request.session.get(slug) or request.session.get(slug,0) < students_vote_limit() :
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
    else: 
        return redirect(reverse('Student Entry Page'))

# Returns a clean formatted nickname
def formattedNickname(nickname):
    import string
    unwanted_char = ['.',"'",'"','>','<','?',"\\",'/','*','.',',','!','@','#','$','%','^','&','(',')','-','_','+','=','{','}','[',']','|',':',';']
    nickname1 = ''.join((filter(lambda i: i not in unwanted_char, nickname)))
    a=''
    for i in nickname1.split(' '): a += i.capitalize() + ' '
    return a.strip(' ') if a != string.whitespace else False 
