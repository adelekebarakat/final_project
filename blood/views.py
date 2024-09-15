from datetime import timedelta
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from .forms import CustomUserCreationForm, EditProfileForm, EmergencyForm, VerifyPhoneForm, sanitize_phone_number
from .models import Emergency, CanDonateTo, CanReceiveFrom, User, BloodType
from .sms import send_sms, send_verification_code
from .geolocation import get_coordinates
from .utils import generate_verification_code, reverse_geocode
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def SignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.phone_verified = False  
            user.verification_code = generate_verification_code()
            user.verification_code_created_at = timezone.now()
            user.save()
            send_verification_code(user)
            messages.success(request, 'Your account has been created successfully!')
            login(request, user)
            return redirect('verify_phone')
            
            # return redirect('home')
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


        
            if latitude and longitude:
                incident_location_name = reverse_geocode(latitude, longitude, settings.HERE_API_KEY)
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
                message = (
                    f"Case Number: {emergency_request.case_number}\n"
                    f"Emergency blood donation needed. "
                    f"Blood type required: {emergency_request.blood_type}. "
                    # f"Incident location: {incident_location_name}. "
                    f"Location: {filled_location}. "
                    f"Please respond if you can donate."
                )
                success, response_message = send_sms(formatted_phone_number, message)
                if not success:
                    print(f"Failed to send SMS to {formatted_phone_number}: {response_message}")



            return render(request, 'blood/compatible_users.html', {'compatible_users': compatible_users})
            
    
    else:
        form = EmergencyForm()
    return render(request, 'blood/emergencyform.html', {'form': form})


@login_required(login_url='login')
def emergency_list(request):
    emergencies = Emergency.objects.all()
    return render(request, 'blood/emergency_list.html', {'emergencies': emergencies})


@login_required(login_url='login')
def emergency_detail(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)
    return render(request, 'blood/emergency_details.html', {'emergency': emergency})


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