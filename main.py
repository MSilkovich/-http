import sys
from io import BytesIO

import requests
from PIL import Image

def intofile(params):
    f = open("Параметры поиска.txt", 'a')
    f.write(params)
    f.close()
toponym_to_find = "ulitsa_akademika_korolyova_12"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
print(toponym)
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
up = toponym['boundedBy']['Envelope']['lowerCorner'].split()
down = toponym['boundedBy']['Envelope']['upperCorner'].split()
delta1 = str(float(down[0]) - float(up[0]))
delta2 = str(float(down[1]) - float(up[1]))
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta1, delta2]),
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude]),
}
intofile(map_params)
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
