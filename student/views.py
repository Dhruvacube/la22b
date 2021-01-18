import ast

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from main.models import *
from main.views import date_start_end, get_respect_date
from titles.models import *

from .models import *
from .templatetags import extras

total_students = lambda: Student.objects.filter(hidden=False).count()
students_vote_limit = lambda: Settings.objects.values('nickname_limit').get_or_create()[0]['nickname_limit']

def photo(class_stu):
    if class_stu == 'SC-1': return 'class/sc_1.jpeg'
    elif class_stu == 'SC-2': return 'class/sc_2.jpeg'
    elif class_stu == 'SC-3': return 'class/sc_3.jpeg'
    elif class_stu == 'COMMERCE': return 'class/commerce.jpeg'
    elif class_stu == 'ARTS': return 'class/arts.jpeg'

# Create your views here.

#Student entry View
def entry(request):
    classes = Student.objects.values('class_stu').distinct('class_stu')
    return render(
        request,
        'class.html',
        {
            'total_students': total_students,
            'image': 'class/sc_1.jpeg',
            'classes': classes,
        }
    )

def student_class_wise(request,class_stu):
    student_model = Student.objects.filter(hidden=False,class_stu=class_stu.upper()).all()
    return render(
        request,
        'student-entry.html',
        {
            'total_students': total_students,
            'student_model': student_model,
            'class_stu':class_stu,
        }
    )

def search(request):
    if request.method == 'GET':
        query = formattedNickname(request.GET['query'])
        if len(query)>350:
            stu_list = Student.onjects.none()
            messages.warning(request, "Please limit your query to 350 characters or less only!")

        stuName = Student.objects.filter(name__icontains=query.strip(' '),hidden=False)
        stuClass = Student.objects.filter(class_stu__icontains=query.strip(' '),hidden=False)
        stutitle = Student.objects.filter(data__icontains=query.strip(' '),hidden=False)

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
def student(request, class_stu ,slug):
    student = get_object_or_404(Student,slug=slug,hidden=False,class_stu=class_stu.upper())
    titles = Titles.objects.filter(gender=student.gender, title_stu=student.class_stu).all()
    titles_all = Titles.objects.filter(gender='ALL',title_stu='ALL').all()

    t1 = ast.literal_eval(student.data).get('titles')
    t = t1 if t1 else ['Dummy','List'] 

    return render(
        request,
        'student-profile.html',
        {
            'student':student,
            'titles':titles.union(titles_all),
            'slug':slug,
            'data' : t,
            'titles_404': False if titles.count() else True,
            'data_404': False if len(ast.literal_eval(student.data) if student.data else []) else True,
            'total_students':total_students,
            'profile_stu': True,
            'date_start_end': date_start_end,
            'starts_end': get_respect_date()[1],
            'get_date': str(get_respect_date()[0].strftime("%b %d, %Y %X")),
            'photo': photo(student.class_stu)
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
                            vote = int(i[-1] + 1)
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
