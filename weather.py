import requests
import json

from matplotlib.font_manager import json_dump

# OpenWeatherMap API: https://openweathermap.org/current

# TODO: Sign up for an API key
OWM_API_KEY = '62d326640bcae67b9575cc115e7ec392' # OpenWeatherMap API Key

DEFAULT_ZIP = 90089

def get_weather(zip_code):

    # Getting the lat and lon vlaues from a zip code
    coordinate_params = {
        'appid': OWM_API_KEY,
        'zip': str(zip_code) + ",US"
    }

    coordinate_response = requests.get('http://api.openweathermap.org/geo/1.0/zip', coordinate_params)

    if coordinate_response.status_code == 200: # Status: OK
        coords = coordinate_response.json()
    else:
        print('error: got response code %d' % coordinate_response.status_code)
        print(coordinate_response.text)
        return -1, -1

    params = {
        'appid': OWM_API_KEY,
        'lat': coords["lat"],
        'lon': coords["lon"], 
        'units': "imperial"
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()
        return data["weather"][0]["main"], data["clouds"]["all"]

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return -1, -1

def weather_init():
    zip_code = DEFAULT_ZIP
    weather, cloudiness = get_weather(zip_code)
    
    data = {
        'weather' : weather,
        'cloudiness' : cloudiness
    }

    print(data)

    return json.dumps(data)


WEATHER_APP = {
    'name': 'Weather',
    'init': weather_init
}


if __name__ == '__main__':
    weather_init()