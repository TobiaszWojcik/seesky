import requests
import math


class NominatimGeocoding:
    def __init__(self, address):
        self.API_URL = 'https://nominatim.openstreetmap.org/search.php?q={}&format=json&limit=1'
        response = requests.get(self.API_URL.format(address))
        self.geolocation_dict = response.json()[0]

    def __str__(self):
        return str(self.geolocation_dict.get('display_name'))

    def lat(self):
        return round(float(self.geolocation_dict['lat']), 6)

    def lon(self):
        return round(float(self.geolocation_dict['lon']), 6)

class CalkDistance:
    def __init__(self):
        self.EARTH_R = 6378137

    def distance(self, latlong_a:list, latlong_b:list):
        lat_a = float(latlong_a[0])
        lon_a = float(latlong_a[1])
        lat_b = float(latlong_b[0])
        lon_b = float(latlong_b[1])
        d_lat = math.radians(lat_a) - math.radians(lat_b)
        d_long = math.radians(lon_a) - math.radians(lon_b)

        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) +\
            math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) *\
            math.sin(d_long / 2) * math.sin(d_long / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.EARTH_R * c
        return distance


