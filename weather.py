import requests
import json
import re
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from geopy.geocoders import Nominatim

app = Flask(__name__)


class Weather:

    def __init__(self, app_name, api_key, server,
                 city_name=False, debug=True):
        self.app_name = app_name
        self.city_name = city_name
        self.api_key = api_key
        self.server = server
        self.weather_data = []
        self.refresh(self.city_name)
        self.debug = debug
        self.default_city = 'Moscow'

    def manager_city(self, city_name_):
        geolocator = Nominatim(user_agent=self.app_name)
        location = geolocator.geocode(city_name_)
        if location is None:
            location = geolocator.geocode(self.default_city)
        return (location.latitude, location.longitude)

    def refresh(self, city_name_, metric='metric'):
        try:
            if len(str(city_name_)) < 3:
                city_name_ = self.default_city
            lat, lon = self.manager_city(city_name_)
            self.settings = {'appid': self.api_key,
                             'units': metric,
                             'exclude': 'daily',
                             'lang': 34}
            self.select_auto_server(city_name_, lat, lon)
            response = requests.get(self.server, params=self.settings)
            self.weather_data = json.loads(response.text)
            print(self.weather_data)
            self.set_settings()
            self.set_city_name(city_name_)
            self.set_wind_setting()
        except IOError as error:
            print('Class Weather Error connect:', error)
            self.weather_data = {'cod': '0000',
                                 'message': error}

    def select_auto_server(self, city_name_, lat, lon):
        if re.search('onecall', self.server):
            _lat_lon = {'lon': lon, 'lat': lat}
            _settings = self.settings.copy()
            _settings.update(_lat_lon)
            self.settings = _settings
        elif re.search('weather', self.server):
            _query = {'q': city_name_}
            _settings = self.settings.copy()
            _settings.update(_query)
            self.settings = _settings

    def set_city_name(self, _city_name):
        self.city_name = _city_name

    def set_wind_setting(self):
        self.wind_setting = 'm/s'

    def set_settings(self):
        if 'units' in self.settings:
                if self.settings['units'] == 'metric':
                    self.temp_settings = '°C'
                elif self.settings['units'] == 'imperial':
                    self.temp_settings = '°F'
                else:
                    self.temp_settings = 'K'
        else:
            self.temp_settings = 'K'

    def content(self, format_time='%Y-%m-%d %H:%M:%S'):
        if (len(self.weather_data) != 0) and (
                              'message' not in self.weather_data):
            _content = {'app_name': self.app_name,
                        'city': self.city(),
                        'temp': str(self.temp()) + self.temp_settings,
                        'pressure': self.pressure(),
                        'speed_wind': str(
                                 self.speed_wind()) + self.wind_setting,
                        'date': self.timestamp(format_time),
                        'deg_wind': str(self.deg_wind()),
                        'ai': self.ai()}
            return _content
        elif ('message' in self.weather_data):
            return self.error_log()

    def error_log(self):
        if self.weather_data['cod'] == '0000':
            if self.debug:
                debug_message = self.weather_data['message']
            else:
                debug_message = 'pleas debug True more information'
            return {'app_name': self.app_name,
                    'message': 'Error connect',
                    'cod': debug_message}
        if self.weather_data['cod'] == '404':
            return {'app_name': self.app_name,
                    'message': 'City not found',
                    'cod': self.weather_data['cod']}
        else:
            return {'app_name': self.app_name,
                    'message': 'Error content',
                    'cod': self.weather_data['cod']}

    def ai(self):
        temp = int(self.temp())
        ai_answer = {-60: 'Наступил ледниковый период',
                     -30: 'Даже медведям холодно:)',
                     -25: 'Оденьте шубу',
                     -15: 'Нужна телогрейка',
                     -8: 'Куртка теплая вам пригодится',
                     0: 'Холодно, наденьте куртку',
                     10: 'Вам нужен свитер очень теплый',
                     18: 'Прохладно, лучше утеплится',
                     25: 'Шорты и майка ваша одежда',
                     30: 'Жара выходите в плавках:)',
                     68: 'Пустыня Деште-Лут, на юго-востоке Ирана'}
        number = (min((abs(n-temp), n) for n in ai_answer.keys())[1])
        return ai_answer[number]

    def temp(self):
        if 'main' not in self.weather_data:
            return self.weather_data['current']['temp']
        return self.weather_data['main']['temp']

    def pressure(self):
        if 'main' not in self.weather_data:
            return self.weather_data['current']['pressure']
        return self.weather_data['main']['pressure']

    def deg_wind(self):
        if 'main' not in self.weather_data:
            _wind = self.weather_data['current']['wind_deg']
        else:
            _wind = self.weather_data['wind']['deg']
        _tend = ['Север', 'Северо-Восток', 'Восток',
                 'Юго-Восток', 'Юг', 'Юго-Запад',
                 'Запад', 'Северо-Запад']
        _index = (round(_wind*8/360) % 8)
        return _tend[int(_index)]

    def speed_wind(self):
        if 'main' not in self.weather_data:
            return self.weather_data['current']['wind_speed']
        return self.weather_data['wind']['speed']

    def city_geolocator(self):
        if 'lat' and 'lon' in self.settings:
            lat_lon = (self.settings['lat'], self.settings['lon'])
            geolocator = Nominatim(user_agent=self.app_name)
            location = geolocator.reverse(lat_lon)
            return location.raw

    def city(self):
        if 'name' not in self.weather_data:
            return self.city_geolocator()['address']['city']
        return self.weather_data['name']

    def timestamp(self, format_time):
        if 'dt' not in self.weather_data:
            date_ = self.weather_data['current']['dt']
        else:
            date_ = self.weather_data['dt']
        _timestamp = datetime.fromtimestamp(date_)
        _timestamp = _timestamp.strftime(format_time)
        return _timestamp


@app.route('/', methods=['GET', 'POST'])
def mini_weather():
    app_name = 'Weather Mini'
    city_name = 'Krasnodar'
    api_key = 'a5f756f97a8cf1082787e8d36699c449'
    server = 'http://api.openweathermap.org/data/2.5/onecall'
    weather = Weather(app_name, api_key, server, city_name, debug=True)
    if request.method == 'POST':
        city_name = request.form['city']
        weather.refresh(request.form['city'])
    return render_template('index.html', **weather.content())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
