from datetime import date, timedelta
from suntime import Sun
from django.shortcuts import render
from .map_finder import NominatimGeocoding
from .satelite import SpaceObject, SpaceDB
from .models import SpaceObjects, Positions
from .add_news import NewsletterSave, ValidEmail
from django.contrib.sites.shortcuts import get_current_site


def about_page(request):
    context = {'title': 'O Projekcie'
               }
    return render(request, 'main.html', context)

def contact_page(request):
    context = {'title': 'Kontak'
               }
    return render(request, 'main.html', context)


def main_page(request):
    context = {'title': 'Strona główna',
               'action': 'show/'}
    return render(request, 'main.html', context)


def show_page(request):
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
            place = NominatimGeocoding(request.POST['place'])
            if not place.error:
                context['error'] = False
                context['lon'] = place.lon()
                context['lat'] = place.lat()
                context['place'] = str(place)
            else:
                context['error_text'] = 'Nie znaleziono takiego miejsca'
        elif request.POST.get('place_name'):
            newsletter_save = NewsletterSave(request.POST)
            context['email'] = request.POST['email']
            site_url = get_current_site(request).domain
            print(site_url)
            if newsletter_save.check(site_url):
                return render(request, 'save.html', context)
            else:
                context['error_text'] = newsletter_save.error
                context['lon'] = request.POST['lon']
                context['lat'] = request.POST['lat']
                context['place'] = request.POST['place_name']
                context['error'] = False
                context['name'] = request.POST['name']

    return render(request, 'newsletter.html', context)


def validate(request, email, token):
    ve = ValidEmail()
    context = {
        'title': 'Potwierdzenie',
        'content': ve.confirm(email, token)
    }
    return render(request, 'confirmation.html', context)


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
