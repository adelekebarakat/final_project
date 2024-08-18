import requests
from decouple import config

def reverse_geocode(latitude, longitude, api_key):
    # Construct the URL using the provided API key
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['formatted_address']
    
    return None