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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email-id'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
        self.fields['blood_type'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    username = forms.TextInput()
    email = forms.EmailField(max_length=150)
    phone_number = forms.NumberInput()
    blood_type = forms.Select()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'phone_number', 'blood_type', 'password1', 'password2')



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

        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'reason_for_request': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'provide Additional location'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number:
            sanitized_contact_number = sanitize_phone_number(contact_number)
            return sanitized_contact_number
        return contact_number



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'blood_type']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            sanitized_phone_number = sanitize_phone_number(phone_number)
            return sanitized_phone_number
        return phone_number


class VerifyPhoneForm(forms.Form):
    verification_code = forms.CharField(max_length=6, label="Verification Code", help_text="Enter the 6-digit code sent to your phone.")