# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User, Emergency
# import phonenumbers
# from phonenumbers import NumberParseException, is_possible_number, is_valid_number

# def sanitize_phone_number(phone_number, region='US'):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, region)
#         if is_possible_number(parsed_number) and is_valid_number(parsed_number):
#             formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
#             # Remove the '+' sign
#             return formatted_number.lstrip('+')
#         else:
#             raise ValueError('Invalid phone number')
#     except NumberParseException:
#         raise ValueError('Failed to parse phone number')
#     except ValueError as e:
#         # Handle invalid number format
#         return str(e)


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'Phone_number', 'blood_type', 'password1', 'password2')

# class EmergencyForm(forms.ModelForm):
#     class Meta:
#         model = Emergency
#         fields = ['blood_type', 'reason_for_request', 'location', 'contact_number']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Emergency
import phonenumbers
from phonenumbers import NumberParseException, is_possible_number, is_valid_number

def sanitize_phone_number(phone_number, region='NG'):
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        if is_possible_number(parsed_number) and is_valid_number(parsed_number):
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            # Remove the '+' sign
            return formatted_number.lstrip('+')
        else:
            raise ValueError('Invalid phone number')
    except NumberParseException:
        raise ValueError('Failed to parse phone number')
    except ValueError as e:
        # Handle invalid number format
        return str(e)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'blood_type', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            sanitized_phone_number = sanitize_phone_number(phone_number)
            return sanitized_phone_number
        return phone_number

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['blood_type', 'reason_for_request', 'location', 'contact_number']

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number:
            sanitized_contact_number = sanitize_phone_number(contact_number)
            return sanitized_contact_number
        return contact_number
