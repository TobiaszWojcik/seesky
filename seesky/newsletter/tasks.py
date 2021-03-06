import datetime
from celery import shared_task
from suntime import Sun
from .models import SpaceObjects, Positions
from .satelite import SpaceObject, SpaceDB
from .email_handler import EmailHandler
from .models import Newsletter
"""
Set of functions responsible for handling periodic tasks.
"""


@shared_task
def reload_space_db():
    """
    Function responsible for the daily retrieval of the predicted locations of space objects and the removal of out-of-date information
    :return: none
    """
    sot = SpaceObject()
    if sot.get_stations():
        SpaceObjects.objects.all().delete()
        for row in sot.station_list:
            SpaceObjects.objects.create(name=row['name'], short=row['short'])
        if sot.get_location():
            Positions.objects.filter(time__lte=(datetime.date.today() + datetime.timedelta(days=-3))).delete()
            for row in sot.positions:
                Positions.objects.create(
                        short=row.get('so_id'),
                        lat=row.get('lat'),
                        lon=row.get('lon'),
                        time=row.get('time_s')
                        )


@shared_task
def email_send():
    """
    Function responsible for the daily sending of emails with the newsletter
    :return: none
    """
    time = datetime.datetime.now().strftime("%H:00:00")
    news_list = Newsletter.objects.filter(email_time=time, valid=True)
    email_h = EmailHandler()
    for obj in news_list:
        db = SpaceDB(float(obj.lat), float(obj.lon))
        sun = Sun(float(obj.lat), float(obj.lon))
        sunset = sun.get_local_sunset_time()
        sunrise = sun.get_local_sunrise_time(datetime.date.today() + datetime.timedelta(days=1))
        sat = db.get_info(sunset, sunrise)
        email_h.newsletter_email(obj, sat, sunset, sunrise)

@shared_task
def reload_space_db_first_time():
    """
    Function responsible for getting the first information
    :return: none
    """
    sot = SpaceObject()
    if sot.get_stations():
        SpaceObjects.objects.all().delete()
        for row in sot.station_list:
            SpaceObjects.objects.create(name=row['name'], short=row['short'])
        if sot.get_location(0):
            for row in sot.positions:
                Positions.objects.create(
                        short=row.get('so_id'),
                        lat=row.get('lat'),
                        lon=row.get('lon'),
                        time=row.get('time_s')
                        )
