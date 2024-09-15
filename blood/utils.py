# import requests
# from decouple import config

# def reverse_geocode(latitude, longitude, api_key):
#     # Construct the URL using the provided API key
#     url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
    
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         results = response.json().get('results')
#         if results:
#             return results[0]['formatted_address']
    
#     return None
import random
import requests

def reverse_geocode(latitude, longitude, api_key):
    # Construct the URL using the HERE API key
    url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={latitude},{longitude}&apikey={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get('items')
        if results:
            return results[0]['address']['label']
    
    return 'Location not available'



def generate_verification_code(length=6):
    """Generate a random numeric verification code."""
    return ''.join(random.choices('0123456789', k=length))
