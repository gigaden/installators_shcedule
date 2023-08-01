from geopy.geocoders import Nominatim


def get_coordinates(address: str):
    geolocator: Nominatim = Nominatim(user_agent='gps')
    location: geolocator = geolocator.geocode(address)
    try:
        coordinates: tuple = location.latitude, location.longitude
        return coordinates
    except:
        return False
