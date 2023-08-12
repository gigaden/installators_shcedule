import openrouteservice
from openrouteservice.directions import directions

import requests
import json
from environs import Env

env = Env()
env.read_env()
token = env('GIS_TOKEN')


# получаем через api пройденное расстояние
def find_distance(coordinates: list[tuple]) -> float:
    coordinates = [[coords[1], coords[0]] for coords in coordinates]
    body = {"coordinates": coordinates}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248d30dd111ec434d0d860053a6a4860435',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=body, headers=headers)

    routes = json.loads(call.text)
    total_distance = routes['routes'][0]['summary']['distance'] / 1000
    return total_distance


# первая версия получения пройденного расстояния.
# Тратит больший лимит api, т.к. отправляет новый запрос между каждыми адресами
# def find_distanceV0(coordinates: list[tuple]) -> float:
#     client = openrouteservice.Client(key=token)
#     first = 0
#     second = 1
#     total_distance = 0
#     while second < len(coordinates):
#         coords: list = [[coordinates[first][1], coordinates[first][0]],
#                         [coordinates[second][1], coordinates[second][0]]]
#         routes: directions = directions(client, coords)
#         distance_km: float = routes['routes'][0]['summary']['distance'] / 1000
#         total_distance += distance_km
#         first = second
#         second += 1
#     return total_distance
