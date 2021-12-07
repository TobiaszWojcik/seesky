from math import fabs
from django.shortcuts import render
from django.http import HttpResponse
from .map_finder import NominatimGeocoding
from .custom_calculations import Calculate
from .satelite import SpaceObject
from .models import SpaceObjects, Positions


def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    calc = Calculate()
    info = []
    if not place.error:
        temp_short = None
        satind = 1
        for obj in Positions.objects.all():
            p_lon, p_lat, o_lon, o_lat = calc.prepare(place.lon(), place.lat(), obj.lon, obj.lat)
            if temp_short and temp_short == obj.short:
                if (t_lon * o_lon) < 0 and fabs(t_lon - o_lon) > 270:
                    if t_lon < o_lon:
                        t_lon += 360
                    else:
                        t_lon -= 360
                tt_lat = t_lat - o_lat

                if tt_lat == 0:
                    tt_lat = 0.00000000001
                f_a = (t_lon - o_lon)/tt_lat
                f_b = t_lon - (f_a*t_lat)
                if f_a == 0:
                    f_a = 0.00000000001
                d_a = -1/f_a
                d_b = p_lon-(d_a*p_lat)
                x_lat = (d_b-f_b)/(f_a-d_a)
                x_lon = f_a * x_lat + f_b
                if calc.is_betwen(t_lat, o_lat, x_lat):
                    if calc.is_betwen(t_lon, o_lon, x_lon):
                        distance = calc.distance(p_lat, p_lon, x_lat, x_lon)
                        if distance < 1000:
                            observation_dir = calc.direction(p_lat, p_lon, x_lat, x_lon)
                            travel_dir = calc.direction(o_lat, o_lon, t_lat, t_lon)
                            obj_speed = calc.distance(o_lat, o_lon, t_lat, t_lon)

                            info.append(f'{satind}.{obj.short} - odległość najbliższa {distance} - w kierunku '
                                        f'{observation_dir}° {obj.time} Kierunek {travel_dir}° Prędkość {obj_speed}')
                            satind += 1

            temp_short = obj.short
            t_lat = o_lat
            t_lon = o_lon
            # temp_time = obj.time
            # distance = calc.distance(place.lat(), place.lon(), obj.lat, obj.lon)
            # kierunek = calc.direction(place.lat(), place.lon(), obj.lat, obj.lon)
            #
            #
            # if distance < 2000:
            #     temp_info = f'{obj.short} będzie w kierunku {kierunek[1]}({kierunek[0]}°) w odległości {distance}' \
            #                 f'km ok godziny {obj.time}.'
            #
            #     temp_speed = calc.distance(temp_lat, temp_long, obj.lat, obj.lon)/5
            #     temp_dir = calc.direction(temp_lat, temp_long, obj.lat, obj.lon)
            #     temp_info += f'Obiekt porusza się z prędkością {temp_speed}km/m w kierunku
            #     {temp_dir[1]}({temp_dir[0]}°)'
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
