from leaveManagementSys.models import LeaveRequest
from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created {username}!')
            return HttpResponseRedirect(reverse('list-lms-admin'))
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    data = request.user.leaverequest_set.all()
    eligible_leave = LeaveRequest.objects.filter(
        applied_user=request.user)
    return render(request, 'users/profile.html', {'data': data, 'eligible_leave': eligible_leave})
