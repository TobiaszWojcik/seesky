import requests
import datetime


class SunsetSunrise:

    def __init__(self):
        self.API_URL = 'https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'
        self.today = datetime.date.today()
        self.tomorrow = datetime.date.today()+datetime.timedelta(days=1)
        self.set = ""
        self.rise = ""

    def rise_set(self, lat, lon):
        response = requests.get(self.API_URL.format(lat, lon, self.today))
        self.set = response.json().get('results').get('sunset')
        response = requests.get(self.API_URL.format(lat, lon, self.tomorrow))
        self.rise = response.json().get('results').get('sunrise')
        s_time = datetime.datetime.strptime(self.set, '%I:%M:%S %p').time()
        r_time = datetime.datetime.strptime(self.rise, '%I:%M:%S %p').time()
        self.set = datetime.datetime.combine(self.today, s_time)
        self.rise = datetime.datetime.combine(self.tomorrow, r_time)

        return [self.set, self.rise]



