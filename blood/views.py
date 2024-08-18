from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from .forms import CustomUserCreationForm, EmergencyForm, sanitize_phone_number
from .models import Emergency, CanDonateTo, CanReceiveFrom, User, BloodType
from .sms import send_sms
from .geolocation import get_coordinates
from .utils import reverse_geocode
# Create your views here.

def SignUpView(request):
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
    return render(request, 'blood/signup.html', context)
    
def SignInView(request):
    return render(request, 'blood/signin.html')

def Home(request):
    return render(request, 'blood/home.html')

@login_required
def Create_emergency_request(request):
    compatible_users = None
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            emergency_request = form.save(commit=False)
            emergency_request.user = request.user
            emergency_request.contact_number = sanitize_phone_number(emergency_request.contact_number, 'NG')

            # Get coordinates from location using the separated function
            # latitude, longitude = get_coordinates(emergency_request.location)
            # emergency_request.latitude = latitude
            # emergency_request.longitude = longitude
            
            # Get latitude and longitude from the form data
            # latitude = request.POST.get('latitude')
            # longitude = request.POST.get('longitude') # Get latitude, longitude, and filled location from the form data
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            filled_location = emergency_request.location  # This is the location filled in the form


            # If latitude and longitude are provided, save them
            # if latitude and longitude:
            #     emergency_request.latitude = latitude
            #     emergency_request.longitude = longitude

            # emergency_request.save()
            # Reverse geocode to get place name or address
            if latitude and longitude:
                incident_location_name = reverse_geocode(latitude, longitude, settings.GOOGLE_MAPS_API_KEY)
            else:
                incident_location_name = 'Location not available'

            emergency_request.save()


            # Find compatible donors based on the blood type
            blood_type = emergency_request.blood_type
            compatible_blood_types = CanReceiveFrom.objects.filter(blood_type=blood_type).values_list('can_receive_from', flat=True)
            compatible_users = User.objects.filter(blood_type__in=compatible_blood_types)
            
            # Send SMS to compatible users
            # for user in compatible_users:
            #     formatted_phone_number = sanitize_phone_number(user.phone_number, 'NG')  # Adjust region code as needed
            #     message = f"Emergency blood donation needed for {emergency_request.user}. Blood type required: {emergency_request.blood_type}. Location: {emergency_request.location}. Please respond if you can donate."
            #     success, response_message = send_sms(formatted_phone_number, message)
            #     if not success:
            #         print(f"Failed to send SMS to {formatted_phone_number}: {response_message}")
            for user in compatible_users:
                formatted_phone_number = sanitize_phone_number(user.phone_number, 'NG')
                message = (
                    f"Emergency blood donation needed for {emergency_request.user}. "
                    f"Blood type required: {emergency_request.blood_type}. "
                    f"Incident location: {incident_location_name}. "
                    f"Location provided: {filled_location}. "
                    f"Please respond if you can donate."
                )
                success, response_message = send_sms(formatted_phone_number, message)
                if not success:
                    print(f"Failed to send SMS to {formatted_phone_number}: {response_message}")



            return render(request, 'blood/compatible_users.html', {'compatible_users': compatible_users})
            
    
    else:
        form = EmergencyForm()
    return render(request, 'blood/emergencyform.html', {'form': form})


@login_required
def emergency_list(request):
    emergencies = Emergency.objects.all()
    return render(request, 'blood/emergency_list.html', {'emergencies': emergencies})


@login_required
def emergency_detail(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)
    return render(request, 'blood/emergency_details.html', {'emergency': emergency})

