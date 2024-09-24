import requests
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def sms(formatted_phone_number, message):
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
        logger.info(f"Sending SMS to {formatted_phone_number} with message: {message}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        logger.info(f"Response from Termii: {data}")
        
        if data.get('message') == 'Successfully Sent':
            logger.info(f"SMS sent successfully to {formatted_phone_number}")
            return True, "Message sent successfully"
        else:
            logger.warning(f"Failed to send SMS to {formatted_phone_number}: {data}")
            return False, data.get('message', 'Failed to send SMS')
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending SMS to {formatted_phone_number}: {str(e)}")
        return False, str(e)

    # try:
    #     logger.info(f"Attempting to send SMS to {formatted_phone_number}")
    #     response = requests.post(url, headers=headers, json=payload, timeout=60)
    #     response_data = response.json()
    #     logger.info(f"Termii response: {response_data}")
        
    #     if response.status_code == 200 and response_data.get('status') == 'success':
    #         logger.info(f"SMS sent successfully to {formatted_phone_number}")
    #         return True, "SMS sent successfully"
    #     else:
    #         error_msg = f"Failed to send SMS. HTTP Status: {response.status_code}, Response: {response_data}"
    #         logger.error(error_msg)
    #         return False, error_msg
    # except requests.exceptions.RequestException as e:
    #     error_msg = f"Network-related error occurred while sending SMS: {str(e)}"
    #     logger.exception(error_msg)
    #     return False, error_msg
    # except Exception as e:
    #     error_msg = f"Exception occurred while sending SMS: {str(e)}"
    #     logger.exception(error_msg)
    #     return False, error_msg





# import requests
# from django.conf import settings
# import logging
# from django.contrib import messages
# from .forms import sanitize_phone_number


# logger = logging.getLogger(__name__)

# def send_sms(formatted_phone_number, message):
    
#     url = "https://v3.api.termii.com/api/sms/send"
#     payload = {
#         "to": formatted_phone_number,
#         "from": "Save Life",
#         "sms": message,
#         "type": "plain",
#         "channel": "generic",
#         "api_key": "TLvoMKVDihCBYffrFQNsvUjsWgZWPSjshRFwhBWPvxpkBunYcuUaaUXQuuAUye",
#     }
#     headers = {
#         'Content-Type': 'application/json',
#     }

#     try:
#         logger.info(f"Attempting to send SMS to {formatted_phone_number}")
#         response = requests.post(url, headers=headers, json=payload)
#         response_data = response.json()
#         logger.info(f"Termii response: {response_data}")

#         if response.status_code == 200 and response_data.get('status') == 'success':
#             logger.info(f"SMS sent successfully to {formatted_phone_number}")
#             return True, "SMS sent successfully"
#         else:
#             error_msg = f"Error message from SMS.py: Failed to send SMS. Error: {response_data.get('message', 'Unknown error')}"
#             logger.error(error_msg)
#             return False, error_msg

#     except requests.exceptions.RequestException as e:
#         error_msg = f"Network-related error occurred while sending SMS: {str(e)}"
#         logger.exception(error_msg)
#         return False, error_msg

#     except Exception as e:
#         error_msg = f"Exception occurred while sending SMS: {str(e)}"
#         logger.exception(error_msg)
#         return False, error_msg


# # def send_verification_code(user):
# #     if user.phone_number:
# #         message = f"Your verification code is {user.verification_code}"
# #         success, response_message = send_sms(user.phone_number, message)
# #         if success:
# #             logger.info(f"Verification code sent to {user.phone_number}")
# #         else:
# #             logger.error(f"Failed to send verification code to {user.phone_number}: {response_message}")
# #     else:
# #         messages.error(user, "No phone number provided for verification.")



# import requests
# from django.conf import settings
# import logging
# logger = logging.getLogger(__name__)
# def send_sms(formatted_phone_number, message):
#     url = f"{settings.TERMII_BASE_URL}/api/sms/send"
#     payload = {
#         "to": formatted_phone_number,
#         "from": "Save Life",
#         "sms": message,
#         "type": "plain",
#         "channel": "generic",
#         "api_key": settings.TERMII_API_KEY,
#     }
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     try:
#         logger.info(f"Attempting to send SMS to {formatted_phone_number}")
#         response = requests.post(url, headers=headers, json=payload, timeout=60)
#         response_data = response.json()
#         logger.info(f"Termii response: {response_data}")
#         if response.status_code == 200 and response_data.get('status') == 'success':
#             logger.info(f"SMS sent successfully to {formatted_phone_number}")
#             return True, "SMS sent successfully"
#         else:
#             error_msg = f"Failed to send SMS. Error: {response_data.get('message', 'Unknown error')}"
#             logger.error(error_msg)
#             return False, error_msg
#     except requests.exceptions.RequestException as e:
#         error_msg = f"Network-related error occurred while sending SMS: {str(e)}"
#         logger.exception(error_msg)
#         return False, error_msg
#     except Exception as e:
#         error_msg = f"Exception occurred while sending SMS: {str(e)}"
#         logger.exception(error_msg)
#         return False, error_msg
