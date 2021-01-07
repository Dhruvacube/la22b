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

total_students = lambda: Student.objects.count()

#A simpple function to get if the voting timing has begun or ends 
def date_start_end():
    a = get_object_or_404(Settings)
    return True if a.vote_nicknameassigntime_start > timezone.now() or a.vote_nicknameassigntime < timezone.now() else False

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
        'cover_body': Settings.objects.values('about_entry').get()['about_entry'], 
        }
    )


def animeChar(request):
    return render(
        request,
        'anime-char.html',
        {
            'total_students':total_students,
            'student_objects': Student.objects.values('name','slug','class_stu').all(),
            'randomAnimeChar': randomAnimeChar(),
            'backgroundAnime': randomAnimeChar(),
        }
    )


def animeCharResult(request):
    if request.method == "POST":
        slug = request.POST['name']
        student_obj = get_object_or_404(Student, slug=slug)
        random_anime_char = randomAnimeChar(namelist=(student_obj.gender, student_obj.name))
        return render(
            request,
            'anime-char-result.html',
            {
                'student_model': student_obj,
                'random_anime_char': random_anime_char,
                'backgroundAnime': randomAnimeChar(),
                'display_footer':True,
                'anime_char_name': returnAnimeName(random_anime_char),
                'total_students':total_students,
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

