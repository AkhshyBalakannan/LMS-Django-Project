from django.shortcuts import render
from .models import LeaveRequest

# Create your views here.


def home(request):
    return render(request, 'home.html', {'title': 'ABC HOME'})


def signin(request):
    return render(request, 'signin.html', {'title': 'Signin'})


def lmsadmin(request):
    context = {'details': LeaveRequest.objects.all()}
    return render(request, 'admin_home.html', context)
