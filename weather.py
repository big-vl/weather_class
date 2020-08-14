import requests
import json
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request

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

    def refresh(self, city_name_, metric='metric'):
        try:
            if len(str(city_name_)) < 3:
                city_name_ = 'Moscow'
            self.settings = {'q': city_name_,
                             'appid': self.api_key,
                             'units': metric}
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
        return self.weather_data['main']['temp']

    def pressure(self):
        return self.weather_data['main']['pressure']

    def deg_wind(self):
        _wind = self.weather_data['wind']['deg']
        _tend = ['Север', 'Северо-Восток', 'Восток',
                'Юго-Восток', 'Юг', 'Юго-Запад',
                'Запад', 'Северо-Запад']
        _index = round((_wind/8)/6)
        print(_index)
        return _tend[int(_index)]

    def speed_wind(self):
        return self.weather_data['wind']['speed']

    def city(self):
        return self.weather_data['name']

    def timestamp(self, format_time):
        _timestamp = datetime.fromtimestamp(self.weather_data['dt'])
        _timestamp = _timestamp.strftime(format_time)
        return _timestamp


@app.route('/', methods=['GET', 'POST'])
def mini_weather():
    app_name = 'Weather Mini'
    city_name = 'Krasnodar'
    api_key = 'a5f756f97a8cf1082787e8d36699c449'
    server = 'http://api.openweathermap.org/data/2.5/weather'
    weather = Weather(app_name, api_key, server, city_name, debug=True)
    if request.method == 'POST':
        city_name = request.form['city']
        weather.refresh(request.form['city'])
    return render_template('index.html', **weather.content())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
