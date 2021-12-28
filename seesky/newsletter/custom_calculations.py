import math


class Calculate:
    """
    This class is a set of methods to perform some custom calculations needed for a seesky project to function properly

    Methods:
    * distance - method of calculating distances between two points on the sphere
    * direction - method of calculating direction in degrees betwene two points on a system of coordinates
    * is_between - method tell if one point can lie between two other points in coordinate system
    * prepare - simple custom method returning float and changing values based on parts of a globe
    """
    def __init__(self):
        self.EARTH_R = 6378137
        self.round = 1000  # 1km

    def distance(self, lat_a: float, lon_a: float, lat_b: float, lon_b: float):
        """
        method of calculating distances between two points on the sphere
        :param lat_a: Latitude of first point as float e.g 50,223123
        :param lon_a: Longitude of first point as float e.g 23,123123
        :param lat_b: Latitude of second point as float e.g 50,223123
        :param lon_b: Longitude of second point as float e.g 23,123123
        :return: float distance in km between two points
        """
        lat_a = float(lat_a)
        lon_a = float(lon_a)
        lat_b = float(lat_b)
        lon_b = float(lon_b)
        d_lat = math.radians(lat_a) - math.radians(lat_b)
        d_long = math.radians(lon_a) - math.radians(lon_b)

        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) +\
            math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) *\
            math.sin(d_long / 2) * math.sin(d_long / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # metry
        return int((self.EARTH_R * c)/self.round)  # km

    @staticmethod
    def direction(lat_a: float, lon_a: float, lat_b: float, lon_b: float):
        """
        method of calculating direction in degrees betwene two points on a system of coordinates
        :param lat_a: Latitude of first point as float e.g 50,223123
        :param lon_a: Longitude of first point as float e.g 23,123123
        :param lat_b: Latitude of second point as float e.g 50,223123
        :param lon_b: Longitude of second point as float e.g 23,123123
        :return: method returns list :name of direction as string and int: direction in degree
        """
        lat_a = float(lat_a)
        lon_a = float(lon_a)
        lat_b = float(lat_b)
        lon_b = float(lon_b)

        radians = math.atan2((lon_b - lon_a), (lat_b - lat_a))
        compass = radians * (180 / math.pi)
        coord_names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        coord_dir = round(compass / 45)
        if compass < 0:
            compass += 360
        compass = round(compass)
        if coord_dir < 0:
            coord_dir += 8
        return compass, coord_names[coord_dir]

    @staticmethod
    def is_between(minimum: float, maximum: float, between: float):
        """
        method tell if one point can lie between two other points in coordinate system
        :param minimum: float: first point
        :param maximum: float: second point
        :param between: float: point which you want to check
        :return: boolean
        """
        if maximum > minimum:
            if minimum <= between <= maximum:
                return True
        elif maximum < minimum:
            if minimum >= between >= maximum:
                return True

        return False

    @staticmethod
    def prepare(place_lon, place_lat, obj_lon, obj_lat):
        """
        simple custom method returning float and changing values based on parts of a globe
        :param place_lon:
        :param place_lat:
        :param obj_lon:
        :param obj_lat:
        :return:
        """
        place_lon = float(place_lon)
        place_lat = float(place_lat)
        obj_lon = float(obj_lon)
        obj_lat = float(obj_lat)
        if -90 < place_lon < 90:
            if obj_lon > 180:
                obj_lon -= 360
        else:
            if place_lon < 0:
                place_lon += 360

        return place_lon, place_lat, obj_lon, obj_lat
