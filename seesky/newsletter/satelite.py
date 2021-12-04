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
        self.station_list_name = []
        self.station_list_short = []
        self.station_list_exp_time = []
        self.station_list = []
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
                    self.station_list_name.append(row['Name'])
                    self.station_list_short.append(row['Id'])
                    self.station_list_exp_time.append(time)
                    self.station_list.append({'name': row['Name'], 'short': row['Id'], 'exp_time': time})
            return True
        else:
            return False

    def get_location(self, sats, time: list):
        ssc = self.space_class()

        coord_options = [
                FilteredCoordinateOptions(CoordinateSystem.GEO, CoordinateComponent.LAT),
                FilteredCoordinateOptions(CoordinateSystem.GEO, CoordinateComponent.LON),
                ]
        output_options = OutputOptions(coord_options, None, None, None, None, None, None)

        sats_obj = []

        for sat in sats:
            sats_obj.append(SatelliteSpecification(sat, 30))

        loc_request = DataRequest('Take Satelites', TimeInterval(time[0], time[1]), sats_obj, None, output_options)
        result = ssc.get_locations(loc_request)

        if result['HttpStatus'] == 200:
            obj_table = []
            for obj in result.get('Data'):
                res_id = obj.get('Id')
                res_lat = obj.get('Coordinates')[0].get('Latitude')
                res_lon = obj.get('Coordinates')[0].get('Longitude')
                res_time = obj.get('Time')

                for ix in range(0, (len(res_time))):
                    obj_table.append([res_id, res_lat[ix], res_lon[ix], res_time[ix]])
            return True
        else:
            return False
