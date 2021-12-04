import requests, datetime


class SunsetSunrise:

    def __init__(self):
        self.API_URL = 'https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'
        self.today = datetime.date.today()
        self.tomorrow = datetime.date.today()+datetime.timedelta(days=1)
        self.set = ""
        self.rise = ""

    def rise_set(self, lat, lon):
        response = requests.get(self.API_URL.format(lat,lon, self.today))
        self.set = response.json().get('results').get('sunset')
        response = requests.get(self.API_URL.format(lat, lon, self.tomorrow))
        self.rise = response.json().get('results').get('sunrise')
        return [self.set, self.rise]


sun_s_s = SunsetSunrise()
print(sun_s_s.rise_set('49.556741', '22.211702'))
