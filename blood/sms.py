import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms(formatted_phone_number, message):
    url = f"{settings.TERMII_BASE_URL}/api/sms/send"
    payload = {
        "to": formatted_phone_number,
        "from": "Save Life",
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": settings.TERMII_API_KEY,
    }
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        logger.info(f"Attempting to send SMS to {formatted_phone_number}")
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        logger.info(f"Termii response: {response_data}")

        if response.status_code == 200 and response_data.get('status') == 'success':
            logger.info(f"SMS sent successfully to {formatted_phone_number}")
            return True, "SMS sent successfully"
        else:
            error_msg = f"Failed to send SMS. Error: {response_data.get('message', 'Unknown error')}"
            logger.error(error_msg)
            return False, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Network-related error occurred while sending SMS: {str(e)}"
        logger.exception(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Exception occurred while sending SMS: {str(e)}"
        logger.exception(error_msg)
        return False, error_msg
