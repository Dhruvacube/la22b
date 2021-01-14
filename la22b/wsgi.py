"""
WSGI config for farewellsc1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la22b.settings')

application = get_wsgi_application()

try:
    import uwsgidecorators
    from django.core.management import call_command

    @uwsgidecorators.timer(10)
    def send_queued_mail(num):
        """Send queued mail every 10 seconds"""
        call_command('send_queued_mail', processes=1)
        call_command('remove_stale_queries')
    
    @uwsgidecorators.timer(10)
    def remove_stale_queries(num):
        call_command('remove_stale_queries')
    
    @uwsgidecorators.timer(86400)
    def remove_profile(num):
        call_command('remove_profile')

except ImportError:
    print("uwsgidecorators not found. Cron and timers are disabled")
