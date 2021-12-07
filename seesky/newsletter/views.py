from math import fabs
from django.shortcuts import render
from django.http import HttpResponse
from .map_finder import NominatimGeocoding
from .custom_calculations import Calculate
from .satelite import SpaceObject
from .models import SpaceObjects, Positions
from .sunset_sunrise import SunsetSunrise


def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    calc = Calculate()
    info = []
    sunset = None
    sunrise = None
    if not place.error:
        sun_action = SunsetSunrise()
        temp_id = 0
        temp_short = None
        max_delat = 15
        satind = 1
        sunset, sunrise = sun_action.rise_set(place.lat(), place.lon())
        max_lat = place.lat() + max_delat
        min_lat = place.lat() - max_delat
        max_lon = place.lon() + max_delat
        if max_lon < 0:
            max_lon = max_lon + 360
        min_lon = place.lon() - max_delat
        if min_lon < 0:
            min_lon = min_lon + 360
        if min_lon > max_lon:
            objs = Positions.objects.filter(time__gte=sunset,
                                            time__lte=sunrise,
                                            lat__gte=min_lat,
                                            lat__lte=max_lat) \
                    & Positions.objects.exclude(lon__gte=min_lon,
                                                lon__lte=max_lon)
        else:
            objs = Positions.objects.filter(time__gte=sunset,
                                            time__lte=sunrise,
                                            lat__gte=min_lat,
                                            lat__lte=max_lat,
                                            lon__gte=min_lon,
                                            lon__lte=max_lon)
        for obj in objs:
            p_lon, p_lat, o_lon, o_lat = calc.prepare(place.lon(), place.lat(), obj.lon, obj.lat)
            if temp_short and temp_short == obj.short and temp_id + 1 == obj.id:
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
                            info.append({
                                'observation_dir': observation_dir,
                                'obj_dir': travel_dir,
                                'obj_speed': obj_speed,
                                'obj_short': temp_short,
                                'obj_time': obj.time,
                            })

                            satind += 1
            else:
                temp_short = obj.short
            temp_id = obj.id
            t_lat = o_lat
            t_lon = o_lon
    context = {
        'title': 'Obiekty w okolicy',
        'place': place,
        'info': info,
        'sunset': sunset,
        'sunrise': sunrise,
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
