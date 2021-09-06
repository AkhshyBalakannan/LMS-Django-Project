'''Views module for user app'''
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from leavemanagementsys.leave_functionalities import leave_details
from users.models import CustomUser
from .forms import UserRegisterForm, UserSelectUpdateForm, UserUpdationForm


@login_required
def register(request):
    '''Register new user'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid() and form.save():
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        messages.warning(request, 'Invalid form')
    form = UserRegisterForm()
    context = {'form': form, 'title': 'Register'}
    return render(request, 'users/signup.html', context)


@login_required
def home(request):
    '''Home page'''
    context = {'title': 'LMS Home'}
    return render(request, 'users/home.html', context)


@login_required
def profile(request):
    '''Leave profile page'''
    context = leave_details(request.user)
    return render(request, 'users/profile.html', context)


@login_required
def user_profile(request):
    '''User profile page'''
    context = {'title': 'User Profile'}
    return render(request, 'users/user_profile.html', context)


@login_required
def select_update_user(request):
    '''Selection for updations'''
    form = UserSelectUpdateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            if not CustomUser.objects.filter(email=email).first():
                messages.warning(request, 'No user found')
                return redirect('select-update-user')
            return HttpResponseRedirect(reverse('update-user', kwargs={'email': email}))
    context = {'form': form, 'title': 'Search User'}
    return render(request, 'users/update_user.html', context)


@login_required
def update_user(request, email):
    '''Update user'''
    to_update_user = CustomUser.objects.filter(email=email).first()
    if request.method == 'POST':
        form = UserUpdationForm(request.POST, instance=to_update_user)
        if form.is_valid() and form.save():
            return redirect('home')
    form = UserUpdationForm(instance=to_update_user)
    context = {'form': form, 'title': 'Update User'}
    return render(request, 'users/update_user.html', context)
