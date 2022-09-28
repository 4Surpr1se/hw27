from geopy.geocoders import Nominatim
from translate import Translator


class GeoFinder(Translator, Nominatim):
    """
     С "Москва, М. Библиотека Имени Ленина" он работал
     время 3 утра разбираться не хочу yaaa
     и похоже, что он дает один и тот же адрес, если и дает
    """

    def __init__(self, location):
        self.location = location
        Translator.__init__(self, to_lang="en", from_lang='ru')
        Nominatim.__init__(self, user_agent='yes')

    def get_lat_lng(self):
        translation = self.translate(self.location)
        location = self.geocode(translation)
        return (location.latitude, location.longitude) if location else (0.0, 0.0)
