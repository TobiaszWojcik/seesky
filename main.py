import datetime
from celery import shared_task
from seesky.newsletter.models import SpaceObjects, Positions
from seesky.newsletter.satelite import SpaceObject
from seesky.newsletter.email_handler import EmailHandler

time = datetime.datetime.now().strftime("%H:00:00")
news_list = Positions.objects.filter(email_time=time)
for obj in news_list:
    print(obj)