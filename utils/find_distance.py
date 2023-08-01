from geopy.geocoders import Nominatim  # Подключаем библиотеку
from geopy.distance import geodesic, great_circle, distance  # И дополнения

from environs import Env

env = Env()
env.read_env()

geolocator = Nominatim(user_agent="Tester")  # Указываем название приложения
# address_1 = str(input('Введите город 1: \n'))  # Получаем название первого города
address_1 = 'нижний новгород, волжская набережная 8'
# address_2 = str(input('Введите город 2: \n'))  # Получаем название второго города
address_2 = 'нижний новгород, июльских дней 3к1'
location_1 = geolocator.geocode(address_1)  # Получаем полное название первого города
location_2 = geolocator.geocode(address_2)  # Получаем полное название второго города
# print('Город 1: ', location_1)  # Выводим первичные данные
# print('Город 2: ', location_2)  # Выводим первичные данные
# print('Координаты города 1: ', location_1.latitude, location_1.longitude)  # Выводим координаты первого города
gps_point_1 = location_1.latitude, location_1.longitude  # Выводим координаты первого города
gps_point_2 = location_2.latitude, location_2.longitude  # Выводим координаты второго города
# print('Координаты города 2: ', location_2.latitude, location_2.longitude)  # Выводим общие данные
# print('Дистанция между городом', location_1, 'и городом ', location_2, ': ',
#       geodesic(gps_point_1, gps_point_2).kilometers, ' километров')  # Выводим полученный результат в километрах
# print('Дистанция между городом', location_1, 'и городом ', location_2, ': ',
#       great_circle(gps_point_1, gps_point_2).kilometers, ' километров')  # Выводим полученный результат в километрах
# print(distance(gps_point_1, gps_point_2).km)

token = env('GIS_TOKEN')
print(gps_point_2, gps_point_1)

# import requests
#
# def matrix(locations: list, profile=0):
#     headers = {
#         'Content-Type': 'application/json; charset=utf-8',
#         'Accept': 'application/json',
#         'Authorization': token
#     }
#     profile_dict = {
#         0: 'driving-car',
#         1: 'foot-walking'
#     }
#     data = {"locations":[i[::-1] for i in locations],"metrics":["distance","duration"],"units":"m"}
#     res = requests.post(f'https://api.openrouteservice.org/v2/matrix/{profile_dict[profile]}',
#                         headers=headers,
#                         json=data).json()
#     return dict(durations = res['durations'][0][1], distances = res['distances'][0][1])
#
# print('\nМОСКВА - УФА на автомобиле')
# result = matrix([[*gps_point_1], [*gps_point_2]], 0)
# print(f'Результат: {result}')
# print(f'Расстояние: ~ {int(result["distances"] / 1000)} км')
# print(f'Время в пути: ~ {int(result["durations"] // 3600)} часов')

import openrouteservice
from openrouteservice.directions import directions
from openrouteservice.distance_matrix import distance_matrix

coords = [[*gps_point_1], [*gps_point_2]]
client = openrouteservice.Client(key=token)  # Specify your personal API key
# routes = directions(client, coords)
#
# print(routes['routes'][0])

routes = distance_matrix(client, coords, profile='driving-car')
print(routes)
