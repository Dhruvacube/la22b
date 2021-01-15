  
"""
 Command for deleting the resolved queries from Contact Model
"""
from datetime import timedelta
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from main.models import RemoveName
from post_office import mail
from post_office.models import EmailTemplate
from student.models import Student


class Command(BaseCommand):
    help = "It hides the requested students from the whole website"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        day_before = timezone.now() - timedelta(days=1)
        hide_model = RemoveName.objects.filter(time_field__lte = day_before).all()
        
        print('\nStudents to be hidden =',f'{hide_model.count()}/{RemoveName.objects.count()}','\n')

        if not EmailTemplate.objects.filter(name='removed_student').all():
                EmailTemplate.objects.create(
                        name='removed_student',
                        description="The email template to intimate admin about that a student got removed from the site.",
                        subject='A student got hidden from the site',
                        content=render_to_string('email/removed-user.txt'),
                )
        
        for i,j in enumerate(hide_model):
            print(j.student_models.name, '-',' ',end='')
            for u in range(11): 
                print('-', end='')
                sleep(0.4)
            print(' hiding', end='')
            sleep(1)
            for o in range(8): 
                print('.', end='')
                sleep(0.4)
            print()
            sleep(1)
            Student.objects.filter(name=j.student_models.name).update(hidden=True)
            j.delete()
            mail.send(
                settings.EMAIL_HOST_USER,
                settings.EMAIL_HOST_USER,
                template='removed_student',
                context={
                    'name': j.student_models.name,
                },
            )

        print('\n',hide_model.count(), 'students made hidden.')

