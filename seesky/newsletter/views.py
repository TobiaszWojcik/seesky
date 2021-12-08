from datetime import date, timedelta
from suntime import Sun
from django.shortcuts import render
from django.http import HttpResponse
from .map_finder import NominatimGeocoding
from .satelite import SpaceObject, SpaceDB
from .models import SpaceObjects, Positions
from .forms import NewsletterForm

def main_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    context = {'title': 'Obiekty w okolicy',
               'place': place}
    print(place.error)
    if not place.error:
        db = SpaceDB(place.lat(), place.lon())
        context['place'] = place
        sun = Sun(place.lat(), place.lon())
        sunset = sun.get_local_sunset_time()
        sunrise = sun.get_local_sunrise_time(date.today() + timedelta(days=1))
        context['info'] = db.get_info(sunset, sunrise)
        context['sunset'] = sunset
        context['sunrise'] = sunrise

    return render(request, 'show.html', context)


def newsletter_page(request):
    context = {
        'error': True,
        'error_text': None,
        'title': 'Zapisz się na Newsletter'
    }
    if request.method == 'POST':
        if request.POST.get('place'):
            place = request.POST['place']
            place = NominatimGeocoding(place)
            if not place.error:
                context['error'] = False
                context['lon'] = place.lon()
                context['lat'] = place.lat()
                context['place'] = str(place)
            else:
                context['error_text'] = 'Niestety nie znaleziono takiego miejsca'


    return render(request, 'newsletter.html', context)


def actualizacja(request):

    context = {
        'title': 'Aktualizacja obiektów kosmicznych',
        'content': 'Aktualna lista obserwowanych satelit:'
    }

    sobj = SpaceObjects.objects.all()
    context['objects'] = sobj

    if request.user.is_superuser:
        if request.method == 'POST':
            sot = SpaceObject()
            if sot.get_stations():
                SpaceObjects.objects.all().delete()
                for row in sot.station_list:
                    SpaceObjects.objects.create(name=row['name'], short=row['short'])
                if sot.get_location():
                    Positions.objects.all().delete()
                    for row in sot.positions:
                        Positions.objects.create(
                                short=row.get('so_id'),
                                lat=row.get('lat'),
                                lon=row.get('lon'),
                                time=row.get('time_s')
                                )

                    context['content'] = 'Zaktualizowano listę obiektów i pozyje obiektów kosmicznych'

                else:
                    context['content'] = 'Błąd: Zaktualizowano listę obiektów, nie  zaktualizowano ich pozyji!!'

            else:
                context['content'] = 'Błąd: Nie udało się pobrać obiektów z serwera NASA!'

        else:
            context['content'] = 'Zaktualizuj obiekty latające'
    return render(request, 'actual.html', context)
