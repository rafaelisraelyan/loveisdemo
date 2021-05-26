from geopy.geocoders import Nominatim
from functools import partial


class citySearch:
    def __init__(self, city=None, lon=None, lat=None):
        try:
            geolocator = Nominatim(user_agent='my_request')
            if lat is None and lon is None:
                self.city = city
                location = geolocator.geocode(self.city)
                self.lon = location.longitude
                self.lat = location.latitude
            elif city is None:
                self.lon = lon
                self.lat = lat
                partial(geolocator.reverse, language="ru")
                location = geolocator.reverse(f"{self.lat},{self.lon}")
                self.city = location.raw['address']['city']
        except Exception as e:
            print(e)


'''
if __name__ == '__main__':

    geolocator = Nominatim(user_agent="my_request")

    reverse = partial(geolocator.reverse, language="en")
    location = geolocator.reverse("32.4027308, 48.4199982")
    city = location.raw
    print(city)'''
