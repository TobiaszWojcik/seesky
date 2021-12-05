import math
import requests


class NominatimGeocoding:
    def __init__(self, address):
        self.API_URL = 'https://nominatim.openstreetmap.org/search.php?q={}&format=json&limit=1'
        response = requests.get(self.API_URL.format(address))
        if not response.text == '[]':
            self.geolocation_dict = response.json()[0]
            self.error = False
        else:
            self.error = True

    def __str__(self):
        return str(self.geolocation_dict.get('display_name'))

    def lat(self):
        return round(float(self.geolocation_dict['lat']), 6)

    def lon(self):
        lon = float(self.geolocation_dict['lon'])
        if lon < 0:
            lon += 360
        return round(lon, 6)


class CalkDistance:
    def __init__(self):
        self.EARTH_R = 6378137
        self.max_distance = 1000  # km

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
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return int((self.EARTH_R * c)/self.max_distance)

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


# Latitude: 50.972059 Longitude: 16.929812
# Latitude: 50.038467 Longitude: 19.766158
if __name__ == '__main__':
    calc = CalkDistance()

    print(calc.direction(50.972059, 16.929812, 50.038467, 19.766158))
    print(calc.distance(50.972059, 16.929812, 50.038467, 19.766158))
