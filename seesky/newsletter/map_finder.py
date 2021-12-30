import requests


class NominatimGeocoding:
    """
    This class search geographic coordinates of place through API openstreetmap
    :param address: e.g City, Zip-code, street name, e.t.c
    """
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
        """
        Method returns the latitude of place.
        :return: float
        """
        lat = float(self.geolocation_dict['lat'])
        return round(lat, 6)

    def lon(self):
        """
        Method returns the longitude of place.
        :return: float
        """
        lon = float(self.geolocation_dict['lon'])
        return round(lon, 6)
