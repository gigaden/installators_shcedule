from geopy.geocoders import Yandex
from environs import Env

env = Env()
env.read_env()


def get_coordinates(address: str):
    geolocator: Yandex = Yandex(api_key=env('YANDEX_GEOCODE_TOKEN'))
    location: geolocator = geolocator.geocode(address, lang='ru_RU')
    try:
        coordinates: tuple = location.latitude, location.longitude
        return coordinates
    except:
        return False
