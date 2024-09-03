import requests
from django.conf import settings

def get_coordinates(address):
    api_key =  settings.GOOGLE_MAPS_API_KEY
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(f'{base_url}?address={address}&key={api_key}')
    location_data = response.json()

    if location_data['status'] == 'OK':
        latitude = location_data['results'][0]['geometry']['location']['lat']
        longitude = location_data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None
