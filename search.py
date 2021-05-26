import math
from citysearch import citySearch

def haversine(lat1, lon1, lat2, lon2):
    # расстояние между широтой и долготой
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    # преобразовать в радианы
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
    a = (pow(math.sin(dLat / 2), 2) +

         pow(math.sin(dLon / 2), 2) *

         math.cos(lat1) * math.cos(lat2));

    rad = 6371 #радиус земли
    c = 2 * math.asin(math.sqrt(a))
    return rad * c
# Код теста погрешность 3-20 км (внутри города, 2000 км)
if __name__ == "__main__":
    lat1 = 59.938732
    lon1 = 30.316229
    lat2 = 45.023309000000000
    lon2 = 39.018187000000000
    city1=citySearch(lat=lat1,lon=lon1)
    city2=citySearch(lat=lat2, lon=lon2)
    print(round(haversine(lat1, lon1, lat2, lon2),2), "км. ",' между ',city1.city,' и ',city2.city)