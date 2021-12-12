from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seesky.settings')
app = Celery('seesky')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
#
# @app.task()
# def update_db():
#     from .tasks import reload_space_db
#     reload_space_db()

#
# @app.task()
# def send_email():
#     from newsletter.email_handler import EmailHandler
#     email = EmailHandler()
#     email.validation('tbaztw@gmail.com', 'token', 'tobiasz', 'site')
#     print('sendemail')
