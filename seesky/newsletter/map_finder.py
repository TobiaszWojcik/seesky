import requests


class NominatimGeocoding:
    def __init__(self, address):
        """
        This class search geographic coordinates of place through API openstreetmap
        :param address: e.g City, Zip-code, street name, e.t.c
        """
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
        lat = float(self.geolocation_dict['lat'])
        return round(lat, 6)

    def lon(self):
        lon = float(self.geolocation_dict['lon'])
        return round(lon, 6)
