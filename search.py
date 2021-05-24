import telebot
from telebot import types
import config
import psycopg2
import math

#cursor.execute("SELECT id FROM users WHERE ms_id = (%s)", [message.chat.id])
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
    lat1 = 59.816799833363270
    lon1 = 30.402098990503546
    lat2 = 45.023309000000000
    lon2 = 39.018187000000000
    print(haversine(lat1, lon1, lat2, lon2), "K.M.")