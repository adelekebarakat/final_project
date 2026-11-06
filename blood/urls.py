from django.urls import path
from .views import SignInView, SignUpView, Home, Create_emergency_request, emergency_list, emergency_detail, respond_to_emergency,  SignOutView,EditProfile,verify_phone_view,resend_verification_code

urlpatterns = [
    path('register', SignUpView, name='register'),
    path('login', SignInView, name='login'),
    path('logout/', SignOutView, name="logout"),
    path('edit/profile/', EditProfile, name="edit_profile"),
    path('home', Home, name='home'),
    path('emergency/create/', Create_emergency_request, name='emergency_request'),
    path('emergencies/', emergency_list, name='emergency_list'),
    path('emergency/<int:emergency_id>/', emergency_detail, name='emergency_detail'),
    path(
    'emergency/<int:emergency_id>/respond/',
 respond_to_emergency,
    name='respond_to_emergency'),
    path('verify-phone/', verify_phone_view, name='verify_phone'),
    path('resend-verification-code/', resend_verification_code, name='resend_verification_code'),
]
