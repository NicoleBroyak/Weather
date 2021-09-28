import requests
import datetime

class WeatherForecast():
    """WeatherForecast Class"""
    def __init__(self):
        self.weather = None
        self.weather_archive = dict()
        self.weather_check_dict = dict()
        self.city_name = 'Warszawa'
        self.lat = 52.237049
        self.lon = 21.017532
        self.date_check = bool()
        self.api_key = None
        self.date_in = self.date_input()
        self.date_archive_query = self.date_query(self.date_in)
        if not self.date_archive_query:
            self.api_get(self.lat, self.lon)

    def items(self):
        for date, weather in self.weather_archive.items():
            yield (date, weather)

        
    def __iter__(self):
        for i in self.weather_check_set:
            yield i

    def __setitem__(self, key, value):
        self.weather_archive[key] = value

    def __getitem__(self, key):
        return self.weather_archive.get(key)

    def __repr__(self):
        pass
    
    def __str__(self) -> str:
        dates = list()
        for k in self.weather_archive.keys():
            dates.append(k)
        return f'{dates}'

    def api_key_input(self):
        api = input('Api key:')
        return api

    def date_input(self):
        date_input = input('Date:')
        self.date_check = self.weather_archive_check(date_input)
        return date_input

    def api_get(self, lat, lon):
        api_key = self.api_key_input()
        request = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}"
                        f"&lon={lon}&appid={api_key}&exclude=minutely,current").json()
        for i in request['daily']:
            date = datetime.date.fromtimestamp(i['dt'])
            if str(date) == self.date_in:
                self.weather_check_dict[self.date_in] = set()
                self.weather_check_dict[self.date_in].add(i['weather'][0]['main'])
                self.date_check = True
        for i in request['hourly']:
            date = datetime.date.fromtimestamp(i['dt'])
            if str(date) == self.date_in:
                self.weather_check_dict[self.date_in].add(i['weather'][0]['main'])
                self.date_check = True
        if not self.date_check:
            print(f'Forecast for {self.date_in} not available. Try again later')
            return
        self.api_add_to_dict(self.date_in)

    def weather_archive_check(self, date):
        with open('weather.csv', mode='r') as output:
            for line in output:
                lines = line.split(sep=',')
                lines[-1] = lines[-1].replace('\n','')
                self.weather_archive[(lines[0])] = lines[-1]
                if date == lines[0]:
                    return True
        return False

    def api_add_to_dict(self, date):
        if 'Rain' in self.weather_check_dict[self.date_in]:
            with open('weather.csv', 'a') as file:
                file.write(f'{date},Raining\n')
                print(f'Weather for {date} is: Raining')
                return
        with open('weather.csv', 'a') as file:
            file.write(f'{date},Not Raining\n')
            print(f'Weather for {date} is: Not Raining')

    def date_query(self, date_input):
        for k, v in self.weather_archive.items():
            if k == date_input:
                print("API GET aborted: weather forecas1t already in archive")
                print(f"Weather for date {k} is {v}")
                return v
        return None

wf = WeatherForecast()
print(wf['2021-10-01'])
print('*' * 50)
print(wf.items())
print(tuple(wf.items()))
print('*' * 50)
print(wf)



