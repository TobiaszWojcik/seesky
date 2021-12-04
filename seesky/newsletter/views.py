from django.shortcuts import render
from django.http import HttpResponse
from .my_custom import NominatimGeocoding, CalkDistance
from .satelite import SpaceObject
from .models import SpaceObjects, Positions



def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    calk = CalkDistance()
    info = []
    if not place.error:
        for obj in Positions.objects.all():
            wynik = calk.distance([place.lat(), place.lon()], [obj.lat, obj.lon])
            if wynik < 1000:
                info.append(f'{obj.so_id} będzie w odległości {wynik}km ok godziny {obj.time_s}')
        print('wykonało')

    context = {
        'title': 'Strona główna',
        'place': place,
        'info': info
    }
    if not place.error:
        pass


    return render(request, 'show.html', context)


def newsletter_page(request):
    return HttpResponse('Strona w budowie')


def main_page(request):
    context = {
        'title': 'Strona główna'
    }

    return render(request, 'main.html', context)


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
                    temp_short = None
                    obj = None
                    for row in sot.positions:
                        if temp_short != row.get('so_id'):
                            obj = SpaceObjects.objects.get(short=row.get('so_id'))
                        Positions.objects.create(so_id=obj, lat=row.get('lat'), lon=row.get('lon'), time_s=row.get('time_s'))

                    context['content'] = 'Zaktualizowano listę obiektów i pozyje obiektów kosmicznych'

                else:
                    context['content'] = 'Błąd: Zaktualizowano listę obiektów, nie  zaktualizowano ich pozyji!!'

            else:
                context['content'] = 'Błąd: Nie udało się pobrać obiektów z serwera NASA!'

        else:
            context['content'] = 'Zaktualizuj obiekty latające'
    return render(request, 'actual.html', context)
