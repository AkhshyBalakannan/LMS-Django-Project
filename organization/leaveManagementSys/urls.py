from django.contrib import admin
from django.urls import path
from leaveManagementSys import views

urlpatterns = [
    path('home/', views.home, name="lms-home"),
    path('signin/', views.signin, name='lms-signin'),
    path('lmsadmin/', views.lmsadmin, name='lms-admin'),
]
