  
"""
 Command for deleting the resolved queries from Contact Model
"""
from django.core.management.base import BaseCommand
from main.models import Contact

class Command(BaseCommand):
    help = "It deletes the resolved queries from the contact model"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        from time import sleep

        delete_model = Contact.objects.filter(resolved=True).all()
        print('\nNo of resolved queries = ', f'{delete_model.count()}/{Contact.objects.count()}\n')

        for i,j in enumerate(delete_model):
            print(j.name, '-', j.subject, ' ',end='')
            for i in range(11): 
                print('-', end='')
                sleep(0.4)
            print(' deleting', end='')
            sleep(1)
            for i in range(8): 
                print('.', end='')
                sleep(0.4)
            print()
            sleep(1)
            j.delete()
        print('\n',delete_model.count(), 'queries deleted.')