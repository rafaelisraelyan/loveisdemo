#from citysearch import citySearch

import math

class calculate:
    def __init__(self, la1=None, lo1=None, la2=None, lo2=None, res=None):
        self.la1 = la1
        self.lo1 = lo1
        self.la2 = la2
        self.lo2 = lo2
        self.res = res
        #Рассчёт
        dLat = (la2 - la1) * math.pi / 180.0
        dLon = (lo2 - lo1) * math.pi / 180.0
        la1 = (la1) * math.pi / 180.0
        la2 = (la2) * math.pi / 180.0
        a = (pow(math.sin(dLat / 2), 2) +

             pow(math.sin(dLon / 2), 2) *

             math.cos(la1) * math.cos(la2))
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        res = rad * c
        self.res = res  # Результат рассчёта


'''if __name__ == "__main__":
    lat1 = 59.938732
    lon1 = 30.316229
    lat2 = 45.023309000000000
    lon2 = 39.018187000000000
    city1=citySearch(lat=lat1,lon=lon1)
    city2=citySearch(lat=lat2, lon=lon2)
    print(round(calculate(la1=lat1, lo1=lon1, la2=lat2, lo2=lon2).res,2), "км. ",' между ',city1.city,' и ',city2.city)
    1756.57 км.   между  Санкт-Петербург  и  Краснодар'''