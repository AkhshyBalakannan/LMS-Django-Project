from django.contrib import admin
from django.urls import path
from leaveManagementSys import views

urlpatterns = [
    path('home/', views.Home.as_view(), name="lms-home"),
    path('signin/', views.Signin.as_view(), name='lms-signin'),
    path('employee/<int:pk>/', views.Employee.as_view(), name="employee-home"),
    path('lmsadmin/', views.list_lms_admin, name='list-lms-admin'),
    path('lmsadmin/<int:pk>/', views.detailed_lms_admin, name='detailed-lms-admin'),
]
