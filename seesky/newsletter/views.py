from django.shortcuts import render
from django.http import HttpResponse
from .my_custom import NominatimGeocoding
from .satelite import SpaceObject
from .models import SpaceObjects



def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    context = {
        'title': 'Strona główna',
        'place': place,
    }
    if not place.error:
        pass

    return render(request, 'show.html', context)


def newsletter_page(request):
    return HttpResponse('To jest strona g')


def main_page(request):
    return HttpResponse(f'Długość to ')


def actualizacja(request):

    context = {
        'title': 'Aktualizacja obiektów kosmicznych',
        'content': 'Nie masz uprawnień dla tej strony'
    }
    if request.user.is_superuser:
        sobj = SpaceObjects.objects.all()
        context['objects'] = sobj
        if request.method == 'POST':
            sot = SpaceObjectTaker()
            if sot.get_stations():
                SpaceObjects.destroy_all
                for row in sot.station_list:
                    SpaceObjects.objects.create(name=row['name'], short=row['short'], exp_time=row['exp_time'])
                context['content'] = 'Baza obiektów została zaktualizowana!'
            else:
                context['content'] = 'Błąd: Nie udało się pobrać obiektów z serwera NASA!'
        else:
            context['content'] = 'Zaktualizuj obiekty latające'
    return render(request, 'actual.html', context)