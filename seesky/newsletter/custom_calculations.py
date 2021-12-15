import math


class Calculate:
    def __init__(self):
        self.EARTH_R = 6378137
        self.round = 1000  # 1km

    def distance(self, lat_a, lon_a, lat_b, lon_b):
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
    def direction(lat_a, lon_a, lat_b, lon_b):
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
    def is_betwen(minimum, maximum, betwen):
        if maximum > minimum:
            if minimum < betwen < maximum:
                return True
        elif maximum < minimum:
            if minimum > betwen > maximum:
                return True

        return False

    @staticmethod
    def prepare(place_lon, place_lat, obj_lon, obj_lat):
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
