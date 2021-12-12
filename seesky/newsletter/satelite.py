import datetime
import pytz
from sscws.sscws import SscWs
from sscws.request import DataRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval
from sscws.outputoptions import OutputOptions, FilteredCoordinateOptions
from sscws.coordinates import CoordinateSystem, CoordinateComponent
from .models import Positions
from .custom_calculations import Calculate
from math import fabs


class SpaceObject:
    def __init__(self):
        self.station_list_short = []
        self.station_list = []
        self.positions = []
        self.space_class = SscWs
        self.period = 1  # czas odstępu pomiędzy pomiarami satelit w minutach

# Metoda pobiera informację o satelitach i zwraca tylko te które aktualnie w kosmosie

    def get_stations(self):
        obserwatory = self.space_class()
        obs = obserwatory.get_observatories()
        if obs['HttpStatus'] == 200:
            objects = obs['Observatory']
            now = pytz.utc.localize(datetime.datetime.utcnow())
            for row in objects:
                time = row['EndTime']
                if time > now:
                    self.station_list_short.append(row['Id'])
                    self.station_list.append({'name': row['Name'], 'short': row['Id'], 'exp_time': time})
            return True
        else:
            return False

# Metoda pobiera pozycję satelit pobranych w metodzie get_stations w określonych przedziałach czasowych

    def get_location(self):
        ssc = self.space_class()

        today = datetime.date.strftime(datetime.date.today() + datetime.timedelta(days=1), '%Y%m%dT120000Z')
        tomorrow = datetime.date.strftime(datetime.date.today() + datetime.timedelta(days=2), '%Y%m%dT120000Z')

        coord_options = [
                FilteredCoordinateOptions(CoordinateSystem.GEO, CoordinateComponent.LAT),
                FilteredCoordinateOptions(CoordinateSystem.GEO, CoordinateComponent.LON),
                ]

        output_options = OutputOptions(coord_options, None, None, None, None, None, None)

        status = True
        sats_obj = []
        a = 0
        b = 40
        for sat in self.station_list_short:
            sats_obj.append(SatelliteSpecification(sat, self.period))

        while status:

            loc_request = DataRequest(
                    'Take Satelites',
                    TimeInterval(today, tomorrow),
                    sats_obj[a:b],
                    None, output_options
            )

            result = ssc.get_locations(loc_request)

            a += 40
            if b != 40:
                status = False
            b = None

            if result['HttpStatus'] == 200:
                for obj in result.get('Data'):
                    res_id = obj.get('Id')
                    res_lat = obj.get('Coordinates')[0].get('Latitude')
                    res_lon = obj.get('Coordinates')[0].get('Longitude')

                    res_time = obj.get('Time')
                    for ix in range(0, (len(res_time))):
                        self.positions.append(
                            {'so_id': res_id,
                             'lat': res_lat[ix],
                             'lon': res_lon[ix],
                             'time_s': res_time[ix]})
            else:
                return False
        else:
            return True


class SpaceDB:
    def __init__(self, p_lat, p_lon, search_range=300, max_delat=25):
        self.max_delat = max_delat
        self.p_lat = float(p_lat)
        self.p_lon = float(p_lon)
        self.range = search_range
        self.info = []

    def get_info(self, sunset, sunrise):
        calc = Calculate()
        temp_id = 0
        temp_short = None
        max_lat = self.p_lat + self.max_delat
        min_lat = self.p_lat - self.max_delat
        max_lon = self.p_lon + self.max_delat
        t_lat = None
        t_lon = None
        if max_lon < 0:
            max_lon = max_lon + 360
        min_lon = self.p_lon - self.max_delat
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
            p_lon, p_lat, o_lon, o_lat = calc.prepare(self.p_lon, self.p_lat, obj.lon, obj.lat)
            if temp_short and temp_short == obj.short and temp_id + 1 == obj.id:
                if (t_lon * o_lon) < 0 and fabs(t_lon - o_lon) > 270:
                    if t_lon < o_lon:
                        t_lon += 360
                    else:
                        t_lon -= 360
                tt_lat = t_lat - o_lat
                if tt_lat == 0:
                    tt_lat = 0.00000000001
                # Wyznaczanie parametrów funkcji liniowej y = f_ax+f_b
                f_a = (t_lon - o_lon) / tt_lat
                f_b = t_lon - (f_a * t_lat)
                if f_a == 0:
                    f_a = 0.00000000001
                # wyznaczanie parametrów funkcji liniowej prostopadłej do poprzedniej funkcji (najbliższy punkt)
                d_a = -1 / f_a
                d_b = p_lon - (d_a * p_lat)
                # współrzędne najbliższej odległości od trajektorii obiektu do punktu
                x_lat = (d_b - f_b) / (f_a - d_a)
                x_lon = f_a * x_lat + f_b
                # jaśli najbliższy pkt leży pomiędzy odczytami to wykonaj...
                if calc.is_betwen(t_lat, o_lat, x_lat):
                    if calc.is_betwen(t_lon, o_lon, x_lon):
                        obj_dist = calc.distance(p_lat, p_lon, x_lat, x_lon)
                        # jeśli odległość najbliższa od punktu mniejsza niż ...
                        if obj_dist < 500:
                            observation_dir = calc.direction(p_lat, p_lon, x_lat, x_lon)
                            travel_dir = calc.direction(t_lat, t_lon, o_lat, o_lon)
                            obj_speed = calc.distance(o_lat, o_lon, t_lat, t_lon)
                            self.info.append({
                                'observation_dir': observation_dir[1],
                                'observation_dir_angle': observation_dir[0],
                                'obj_dir': travel_dir[1],
                                'obj_dir_angle': travel_dir[0],
                                'obj_speed': obj_speed,
                                'obj_short': temp_short,
                                'obj_time': obj.time,
                                'obj_dist': obj_dist

                            })
            else:
                temp_short = obj.short
            temp_id = obj.id
            t_lat = o_lat
            t_lon = o_lon
        return self.info
