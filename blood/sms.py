import requests
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def sms(formatted_phone_number, message):
    base_url = settings.TERMII_BASE_URL.rstrip('/')
    url = f"{base_url}/api/sms/send"

    payload = {
        "to": formatted_phone_number,
        "from": "Save Life",
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": settings.TERMII_API_KEY,
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code >= 400:
            logger.error(
        "Termii error: status=%s, response=%s",
        response.status_code,
        response.text
    )
            return False, response.text

        data = response.json()

        # response.raise_for_status()
        # data = response.json()

        if data.get("message") == "Successfully Sent":
            logger.info("Termii accepted SMS successfully.")
            return True, "Message sent successfully"

        logger.warning("Termii rejected SMS: %s", data)
        return False, data.get("message", "Failed to send SMS")

    except requests.exceptions.RequestException as e:
        logger.error("Termii connection error: %s", str(e))
        return False, "Unable to connect to SMS service"

    except ValueError:
        logger.error("Termii returned an invalid response.")
        return False, "Invalid response from SMS service"