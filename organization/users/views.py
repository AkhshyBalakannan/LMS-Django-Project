from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def register(request):
    if request.user.is_manager:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created {username}!')
                return HttpResponseRedirect(reverse('home'))
        else:
            form = UserRegisterForm()
        return render(request, 'users/signup.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('home'))


@login_required
def home(request):
    logged_user = request.user
    return render(request, 'users/home.html', {'user': logged_user})


@login_required
def profile(request):
    logged_user = request.user
    return render(request, 'users/profile.html', {'user': logged_user})
