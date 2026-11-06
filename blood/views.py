from datetime import timedelta
import uuid
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from .forms import CustomUserCreationForm, EditProfileForm, EmergencyForm, VerifyPhoneForm, sanitize_phone_number
from .models import Emergency, EmergencyResponse, CanDonateTo, CanReceiveFrom, User, BloodType
from .sms import sms
from .geolocation import get_coordinates
from .utils import generate_verification_code, reverse_geocode
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def SignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There was an error creating your account. Please try again.')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'blood/signup.html', context)

def SignInView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your desired page after successful login
            else:
                # Handle the case where authentication fails
                return render(request, 'blood/signin.html', {'error': 'Invalid username or password'})
        else:
            # Handle the case where username or password is missing
            return render(request, 'blood/signin.html', {'error': 'Please enter both username and password'})

    return render(request, 'blood/signin.html')


def SignOutView(request):
    logout(request)
    return redirect('login')


def Home(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Successful')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'blood/home.html', context)


from datetime import datetime

def generate_case_number():
    # Generate a case number with the current date and a short UUID
    return f"{str(uuid.uuid4()).split('-')[0].upper()}"


@login_required(login_url='login')
def Create_emergency_request(request):
    compatible_users = None
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            emergency_request = form.save(commit=False)
            emergency_request.user = request.user
            emergency_request.contact_number = sanitize_phone_number(emergency_request.contact_number, 'NG')

            # Get coordinates from location using the separated function
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            filled_location = emergency_request.location  # This is the location filled in the form

            # Generate case number
            if not emergency_request.case_number:
                emergency_request.case_number = generate_case_number()

        
            if latitude and longitude:
                incident_location_name = reverse_geocode(latitude, longitude, settings.GOOGLE_MAP_API)
            else:
                incident_location_name = 'Location not available'
           

            emergency_request.save()


            # Find compatible donors based on the blood type
            blood_type = emergency_request.blood_type
            compatible_blood_types = CanReceiveFrom.objects.filter(blood_type=blood_type).values_list('can_receive_from', flat=True)
            compatible_users = User.objects.filter(blood_type__in=compatible_blood_types)
            
            # Send SMS to compatible users

            for user in compatible_users:
                formatted_phone_number = sanitize_phone_number(user.phone_number, 'NG')
                # case_number = emergency_request.case_number or "N/A"
                location_name = incident_location_name or "Location not available"
                message = (
                    f"Case Number: {emergency_request.case_number}\n"
                    f"Emergency blood donation needed. "
                    f"Blood type required: {emergency_request.blood_type}. "
                    f"Incident location: {incident_location_name}. "
                    f"Location: {filled_location}. "
                    f"Please respond if you can donate."
                )
                success, response_message = sms(formatted_phone_number, message)
                print('success')
    
                if not success:
                    logger.error(f"Failed to send SMS to {formatted_phone_number}: {response_message}")

            return render(request, 'blood/compatible_users.html', {
    'compatible_users': compatible_users,
    'required_blood_type': emergency_request.blood_type,
})
            # return render(request, 'blood/compatible_users.html', {'compatible_users': compatible_users})
    
    else:
        emergency_request = Emergency()
        emergency_request.case_number = generate_case_number()

        form = EmergencyForm(instance=emergency_request)
        
    return render(request, 'blood/emergencyform.html', {'form': form})


@login_required(login_url='login')
def emergency_list(request):
    emergencies = Emergency.objects.all()
    return render(request, 'blood/emergency_list.html', {'emergencies': emergencies})


# @login_required(login_url='login')
# def emergency_detail(request, emergency_id):
#     emergency = get_object_or_404(Emergency, id=emergency_id)
#     return render(request, 'blood/emergency_details.html', {'emergency': emergency})



# Emergency Detail
# @login_required(login_url='login')
# def emergency_detail(request, emergency_id):
#     emergency = get_object_or_404(Emergency, id=emergency_id)

#     is_compatible = False
#     donor_response = None

#     if request.user.is_authenticated and request.user.blood_type:
#         is_compatible = CanReceiveFrom.objects.filter(
#             blood_type=emergency.blood_type,
#             can_receive_from=request.user.blood_type
#         ).exists()

#     if request.user.is_authenticated:
#         donor_response = EmergencyResponse.objects.filter(
#             emergency=emergency,
#             donor=request.user
#         ).first()

#     context = {
#         'emergency': emergency,
#         'is_compatible': is_compatible,
#         'donor_response': donor_response,
#     }

#     return render(request, 'blood/emergency_details.html', context)


@login_required(login_url='login')
def emergency_detail(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)

    is_compatible = False
    donor_response = None

    # Check blood compatibility
    if request.user.blood_type and emergency.blood_type:
        is_compatible = CanReceiveFrom.objects.filter(
            blood_type=emergency.blood_type,
            can_receive_from=request.user.blood_type
        ).exists()

    # Get the logged-in donor's response
    donor_response = EmergencyResponse.objects.filter(
        emergency=emergency,
        donor=request.user
    ).first()

    # Only the emergency requester can see all donor responses
    is_requester = emergency.user == request.user

    donor_responses = None
    willing_count = 0
    unable_count = 0

    if is_requester:
        donor_responses = EmergencyResponse.objects.filter(
            emergency=emergency
        ).select_related('donor', 'donor__blood_type')

        willing_count = donor_responses.filter(
            response='WILLING'
        ).count()

        unable_count = donor_responses.filter(
            response='UNABLE'
        ).count()

    context = {
        'emergency': emergency,
        'is_compatible': is_compatible,
        'donor_response': donor_response,
        'is_requester': is_requester,
        'donor_responses': donor_responses,
        'willing_count': willing_count,
        'unable_count': unable_count,
    }

    return render(request, 'blood/emergency_details.html', context)

# Response to emergency request
@login_required(login_url='login')
@require_POST
def respond_to_emergency(request, emergency_id):

    emergency = get_object_or_404(Emergency, id=emergency_id)

    # Prevent the person requesting blood from responding
    if emergency.user == request.user:
        messages.error(request, "You cannot respond to your own emergency request.")
        return redirect('emergency_detail', emergency_id=emergency.id)

    # Check whether the logged-in donor has a blood type
    if not request.user.blood_type:
        messages.error(request, "Please update your profile with your blood type.")
        return redirect('emergency_detail', emergency_id=emergency.id)

    # Check blood compatibility
    is_compatible = CanReceiveFrom.objects.filter(
        blood_type=emergency.blood_type,
        can_receive_from=request.user.blood_type
    ).exists()

    if not is_compatible:
        messages.error(request, "Your blood type is not compatible with this request.")
        return redirect('emergency_detail', emergency_id=emergency.id)

    # Get the donor's response
    donor_response = request.POST.get('response')

    valid_responses = dict(EmergencyResponse.RESPONSE_CHOICES)

    if donor_response not in valid_responses:
        messages.error(request, "Invalid response. Please try again.")
        return redirect('emergency_detail', emergency_id=emergency.id)

    # Save or update the donor's response
    # Prevent multiple responses to the same emergency
    existing_response = EmergencyResponse.objects.filter(
        emergency=emergency,
        donor=request.user
    ).exists()

    if existing_response:
        messages.warning(
            request,
            "You have already responded to this emergency request."
        )
        return redirect('emergency_list')

    # Save the donor's response
    EmergencyResponse.objects.create(
        emergency=emergency,
        donor=request.user,
        response=donor_response
    )

    messages.success(request, "Your response has been submitted successfully.")
    return redirect('emergency_list')



@login_required(login_url='login')
def EditProfile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            previous_phone = user.phone_number
            form.save(commit=False)
            new_phone = form.cleaned_data.get('phone_number')
            if new_phone and new_phone != previous_phone:
                user.phone_verified = False
                user.verification_code = generate_verification_code()
                user.verification_code_created_at = timezone.now()
                send_verification_code(user)
                messages.info(request, 'A verification code has been sent to your new phone number. Please verify it.')
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'blood/edit_profile.html', {'form': form})


@login_required(login_url='login')
def verify_phone_view(request):
    user = request.user

    if user.phone_verified:
        messages.info(request, "Your phone number is already verified.")
        return redirect('profile')

    if request.method == 'POST':
        form = VerifyPhoneForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            # Check if the code matches and is within the valid time frame (e.g., 10 minutes)
            code_valid = user.verification_code == entered_code
            code_not_expired = user.verification_code_created_at and timezone.now() < user.verification_code_created_at + timedelta(minutes=10)
            if code_valid and code_not_expired:
                user.phone_verified = True
                user.verification_code = None
                user.verification_code_created_at = None
                user.save()
                messages.success(request, "Your phone number has been verified.")
                return redirect('home')
            else:
                messages.error(request, "Invalid or expired verification code.")
    else:
        form = VerifyPhoneForm()

    return render(request, 'blood/verify_phone.html', {'form': form})

@login_required(login_url='login')
def resend_verification_code(request):
    user = request.user
    if user.phone_verified:
        messages.info(request, "Your phone number is already verified.")
        return redirect('home')
    
    user.verification_code = generate_verification_code()
    user.verification_code_created_at = timezone.now()
    user.save()
    send_verification_code(user)
    messages.success(request, "A new verification code has been sent to your phone number.")
    return redirect('verify_phone')