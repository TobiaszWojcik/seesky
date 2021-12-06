from django.shortcuts import render
from django.http import HttpResponse
from .my_custom import NominatimGeocoding, CalkDistance
from .satelite import SpaceObject
from .models import SpaceObjects, Positions


def is_betwen(min,max,betwen):
    if max > min:
        if min < betwen < max:
            return True
    else:
        return False

def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    calk = CalkDistance()
    info = []
    if not place.error:
        temp_short = None
        ind = 1
        for obj in Positions.objects.all():
            lon = float(obj.lon)
            lat = float(obj.lat)
            print(ind)
            ind += 1
            if temp_short and temp_short == obj.short:
                f_a = (temp_long - lon)/(temp_lat - lat)
                f_b = temp_long - (f_a*temp_lat)
                if f_a == 0:
                    f_a = 0.000000001
                d_a = -1/f_a
                d_b = place.lon()-(d_a*place.lat())
                temp_x = (d_b-f_b)/(f_a-d_a)
                temp_y = f_a * temp_x + f_b
                # wynik = calk.distance(place.lat(), place.lon(), temp_x, temp_y)
                # kierunek = calk.direction(place.lat(), place.lon(), temp_x, temp_y)
                # info.append(f'Odległość najbliższa {wynik} w kierunku {kierunek}')
                if is_betwen (temp_lat, lat, temp_x):
                    if is_betwen(temp_long, lon, temp_y):
                        wynik = calk.distance(place.lat(), place.lon(), temp_x, temp_y)
                        kierunek = calk.direction(place.lat(), place.lon(), temp_x, temp_y)
                        info.append(f'{ind}.{obj.short} - odległość najbliższa {wynik} w kierunku {kierunek} {obj.time}')
                        ind += 1
            else:
                ind = 1
            temp_short = obj.short
            temp_lat = lat
            temp_long = lon
            temp_time = obj.time
            # wynik = calk.distance(place.lat(), place.lon(), obj.lat, obj.lon)
            # kierunek = calk.direction(place.lat(), place.lon(), obj.lat, obj.lon)
            #
            #
            # if wynik < 2000:
            #     temp_info = f'{obj.short} będzie w kierunku {kierunek[1]}({kierunek[0]}°) w odległości {wynik}' \
            #                 f'km ok godziny {obj.time}.'
            #
            #     temp_speed = calk.distance(temp_lat, temp_long, obj.lat, obj.lon)/5
            #     temp_dir = calk.direction(temp_lat, temp_long, obj.lat, obj.lon)
            #     temp_info += f'Obiekt porusza się z prędkością {temp_speed}km/m w kierunku {temp_dir[1]}({temp_dir[0]}°)'
            #     info.append(temp_info)


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
