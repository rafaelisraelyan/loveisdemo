from geopy.geocoders import Nominatim
from functools import partial


class citysearch:
    def __init__(self, city=None, lon=None, lat=None):
         if self.lat is None and self.lon is None:
            self.city= city
            geolocator = Nominatim(user_agent='my_request')
            location = geolocator.geocode(self.city)
            self.lon = location.longitude
            self.lat = location.latitude
         elif self.city is None:
            self.lon = lon
            self.lat = lat
            geolocator = Nominatim(user_agent='my_request')
            partial(geolocator.reverse, language="ru")
            location = geolocator.reverse("45.0352566,38.9764814")
            self.city = location.raw['address']['city']


'''
if __name__ == '__main__':

    geolocator = Nominatim(user_agent="my_request")

    reverse = partial(geolocator.reverse, language="ru")
    location = geolocator.reverse("45.0352566,38.9764814")
    city = location.raw['address']['city']
    print(city)'''

