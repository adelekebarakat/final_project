import requests
from decouple import config
import random



def reverse_geocode(latitude, longitude, api_key):
    if not latitude or not longitude or not api_key:
        return 'Location not available'

    url = "https://revgeocode.search.hereapi.com/v1/revgeocode"

    try:
        response = requests.get(
            url,
            params={
                'at': f'{latitude},{longitude}',
                'apikey': api_key
            },
            timeout=10
        )

        response.raise_for_status()

        results = response.json().get('items', [])

        if results:
            return results[0]['address']['label']

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return 'Location not available'

    return 'Location not available'


def generate_verification_code(length=6):
    """Generate a random numeric verification code."""
    return ''.join(random.choices('0123456789', k=length))
