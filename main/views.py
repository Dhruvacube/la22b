from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from student.models import Student

from .models import *
from .forms import *

total_students = lambda: Student.objects.count()

#A simpple function to get if the voting timing has begun or ends 
def date_start_end():
    a = Settings.objects.get_or_create()[0]
    return True if a.vote_nicknameassigntime_start > timezone.now() or a.vote_nicknameassigntime < timezone.now() else False

def get_respect_date():
    a = Settings.objects.get_or_create()[0]
    if a.vote_nicknameassigntime_start > timezone.now():
        return (a.vote_nicknameassigntime_start, 'start')
    elif a.vote_nicknameassigntime < timezone.now():
        return (a.vote_nicknameassigntime,'ends')
    else:
        return (a.vote_nicknameassigntime,'ends')

#To return the count of total confessions
total_confession = lambda : Confession.objects.count()

# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def home(request):
    return render(
        request,
        'cover.html',
        {
            'cover_body': Settings.objects.values('about_entry').get_or_create()[0]['about_entry'], 
        }
    )


def faq(request):
    form = ContactForm()
    remove_form = RemoveProfileForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, 'Query successfully submitted')
        else:
            messages.error(request,'Please correct the errors the below')
    return render(
        request,
        'faq.html',
        {
            'total_students':total_students,
            'settings': Settings.objects.get_or_create()[0],
            'form': form,
            'remove_form': remove_form,
        }
    )

def remove_name_api(request):
    if request.method == "POST":
        form = RemoveProfileForm(request.POST)
        if form.is_valid():
           form.save()
           messages.warning(request, 'Your name has been added to removal list.')
           return redirect(reverse('FAQ'))
        else:
            if form.errors.as_data().get('student_models'):
                messages.warning(request,'Your name is already there in the removal list.')
            else: 
                messages.error(request,'Please correct the errors the below')
            return redirect(request.META.get('HTTP_REFERER'))
    else: return redirect(reverse('FAQ'))

def confession(request):
    confession_model = Confession.objects.order_by('?').all()[:10]
    return render(
        request,
        'fun_games/confession/confession.html',
        {
            'total_students':total_students,
            'confession_model': confession_model,
            'view_more': True if confession_model.count() == 10 else False,
            'fill_colour_list': ['#6f42c1','#e83e8c', '#007bff'],
            'total_confession': total_confession,
            'display_footer': False if total_confession() else True,
            'display_404': False if total_confession() else True,
            'form' : ConfessionForm(),
            'starts_end': get_respect_date()[1],
            'get_date': str(get_respect_date()[0].strftime("%b %d, %Y %X")),
            'date_start_end': date_start_end(),
        }
    )


def confession_more(request):
    confession_model = Confession.objects.order_by('?').all()
    if int(confession_model[:10].count()) < 10: 
        return redirect(reverse('Confession'))
    return render(
        request,
        'fun_games/confession/confession.html',
        {
            'total_students':total_students,
            'confession_model': confession_model,
            'view_more': False,
            'fill_colour_list': ['#6f42c1','#e83e8c', '#007bff'],
            'total_confession': total_confession,
            'form' : ConfessionForm(),
            'starts_end': get_respect_date()[1],
            'get_date': str(get_respect_date()[0].strftime("%b %d, %Y %X")),
            'date_start_end': date_start_end(),
        }
    )


def confession_store(request):
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, 'Confession successfully stored!')
           return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,'Please do not keep the confessions blank or with only special characters!')
            return redirect(request.META.get('HTTP_REFERER'))
    else: return redirect(reverse('Confession'))

def partner(request):
    return render(
        request,
        'fun_games/anime_char/anime-char.html',
        {
            'total_students':total_students,
            'student_objects': Student.objects.values('name','slug','class_stu').all(),
            'randomAnimeChar': randomAnimeChar(),
            'backgroundAnime': randomAnimeChar(),
            'msg_context': 'Find your partner !',
            'btn_name': 'Find',
            'form_submit_url': reverse('Partner Finder Result'),
        }
    )


def partner_result(request):
    if request.method == "POST":
        slug = request.POST['name']
        if slug == 'Select Your Name':
            messages.error(request, "Please select your name from the list !")
            return redirect(reverse('Partner Finder'))
        
        student_obj = get_object_or_404(Student, slug=slug)
        gender = "m" if student_obj.gender == "f" else "f" 
        partner_obj = Student.objects.filter(gender=gender).order_by('?').first()

        return render(
            request,
            'fun_games/partner_finder/partner-result.html',
            {
                'student_model': student_obj,
                'partner_obj': partner_obj,
                'backgroundAnime': randomAnimeChar(),
                'total_students':total_students,
                'message_conxt': 'Matching',
            }
        )
    else: return redirect(reverse('Partner Finder'))


def animeChar(request):
    return render(
        request,
        'fun_games/anime_char/anime-char.html',
        {
            'total_students':total_students,
            'student_objects': Student.objects.values('name','slug','class_stu').all(),
            'randomAnimeChar': randomAnimeChar(),
            'backgroundAnime': randomAnimeChar(),
            'msg_context': 'Which Anime Character are you ?',
            'btn_name': 'Check',
            'form_submit_url': reverse('Which Anime Character are you Results'),
        }
    )


def animeCharResult(request):
    if request.method == "POST":
        slug = request.POST['name']
        if slug == 'Select Your Name':
            messages.error(request, "Please select your name from the list !")
            return redirect(reverse('Which Anime Character are you?'))
        
        student_obj = get_object_or_404(Student, slug=slug)
        random_anime_char = randomAnimeChar(namelist=(student_obj.gender, student_obj.name))
        return render(
            request,
            'fun_games/anime_char/anime-char-result.html',
            {
                'student_model': student_obj,
                'random_anime_char': random_anime_char,
                'backgroundAnime': randomAnimeChar(),
                'anime_char_name': returnAnimeName(random_anime_char),
                'total_students':total_students,
                'message_conxt': 'Checking',
            }
        )
    else: return redirect(reverse('Which Anime Character are you?'))


def returnAnimeName(path_of_pic):
    from student.views import formattedNickname
    if settings.PRODUCTION_SERVER:
        list_path = path_of_pic.split('\\')[-1].split('/')[-1].split('.')[0].replace('_',' ') #heroku specific
    else:
        list_path = path_of_pic.split('\\')[-1].split('.')[0].replace('_',' ')
    return formattedNickname(list_path)


#A function to generate the random anime (optionally a name of the student)
def randomAnimeChar(namelist=None): 
    import os
    import random
    import string
    a = [0,1,2]

    if namelist:
        sex, name = namelist
        folder = 'female' if sex == "f" else "male"
        list_anime_pic = os.listdir(settings.BASE_DIR / os.path.join('main', 'static', 'anime', folder))
        
        nickformatted = name.lower().translate({ord(c): None for c in string.whitespace}) #Removes the whitespace
        no_add = -1 if len(nickformatted)%2 == 0 else 0
        random.seed(random.randint(0,len(name)))
        random_index = random.randint(random.choice(a), len(list_anime_pic)+ no_add)

        return os.path.join('anime', folder, list_anime_pic[random_index])
    
    else: 
        folder = ['female' ,"male"]
        folder_name =  random.choice(folder)
        return os.path.join('anime', folder_name, random.choice(os.listdir(settings.BASE_DIR / os.path.join('main', 'static', 'anime', folder_name))))

