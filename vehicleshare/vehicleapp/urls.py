"""
URL configuration for vehicleshare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vehicleapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.change_profile, name='change_profile'),   
    path('help/', views.help, name='help'),
    path('helpreply/', views.helpreply, name='helpreply'),
    path('ride/', views.ride, name='ride'),
    path('drive/', views.drive, name='drive'),
    path('book/<int:did>', views.book, name='book'),
    path('d_activity/', views.d_activity, name='d_activity'),
    path('r_activity/', views.r_activity, name='r_activity'),
    path('accept/', views.accept, name='accept'),
    path('reject/', views.reject, name='reject'),
    path('request/', views.request, name='request'),
]
