from django.urls import path
from .views import SignInView, SignUpView, Home, Create_emergency_request, emergency_list, emergency_detail

urlpatterns = [
    path('register', SignUpView, name='register'),
    path('login', SignInView, name='login'),
    path('home', Home, name='home'),
    path('emergency/create/', Create_emergency_request, name='emergency_request'),
    path('emergencies/', emergency_list, name='emergency_list'),
    path('emergency/<int:emergency_id>/', emergency_detail, name='emergency_detail'),
]
