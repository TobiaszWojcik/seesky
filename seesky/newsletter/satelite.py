import datetime
import pytz
from sscws.sscws import SscWs
from sscws.request import DataRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval
from sscws.outputoptions import OutputOptions, FilteredCoordinateOptions
from sscws.coordinates import CoordinateSystem, CoordinateComponent


class SpaceObject:
    def __init__(self):
        self.PATH = "https://sscweb.gsfc.nasa.gov/WS/sscr/2/observatories"
        self.station_list_short = []
        self.station_list = []
        self.positions = []
        self.space_class = SscWs

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

    def get_location(self):
        ssc = self.space_class()

        today = datetime.date.strftime(datetime.date.today(), '%Y%m%dT120000Z')
        tomorrow = datetime.date.strftime(datetime.date.today() + datetime.timedelta(days=1), '%Y%m%dT120000Z')

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
            sats_obj.append(SatelliteSpecification(sat, 30))

        while status:


            loc_request = DataRequest('Take Satelites', TimeInterval(today, tomorrow), sats_obj[a:b], None, output_options)
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
                        self.positions.append([res_id, res_lat[ix], res_lon[ix], res_time[ix]])
                        print(res_id, res_lat[ix], res_lon[ix], res_time[ix])

            else:
                return False
        else:
            return True


so = SpaceObject()
if so.get_stations():
    if so.get_location():
        print('udało się')
    else:
        print('nie udało się pobrać pozycji')
else:
    print('nie udało się pobrać stacji')