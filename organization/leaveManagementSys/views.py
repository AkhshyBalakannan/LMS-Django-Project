import leavemanagementsys
from leavemanagementsys.models import LeaveRequest
from django.shortcuts import render
from .forms import RequestLeaveForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser


@login_required
def request_leave(request):
    if request.method == 'POST':
        form = request.POST
        from_date = form.get('fromdate')
        to_date = form.get('todate')
        leave_type = form.get('leavetype')
        description = form.get('description')
        number_of_days = form.get('numofdays')
        leave_request = LeaveRequest.objects.create(applied_user=request.user,
                                                    description=description, from_date=from_date, to_date=to_date, leave_type=leave_type, number_of_days=number_of_days)
        leave_request.save()
        logged_user = request.user
        logged_user.leave_taken += int(number_of_days)
        if logged_user.leave_remaining < 0:
            logged_user.lop_leave_taken += int(number_of_days)
        logged_user.save()
        messages.success(
            request, f'Leave Request Successfully submitted for {description}!')
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'lms/requestLeave.html')


@login_required
def cancel_request(request):
    if request.method == 'GET':
        pk = request.user.id
        print(pk)
        logged_user = CustomUser.objects.get(pk=pk)
        print(logged_user)
        logged_user.objects.LeaveRequest.all()
        print(logged_user)
    elif request.method == 'POST':
        form = request.POST

        description = form.get('description')
        messages.success(
            request, f'Leave Request Successfully cancelled for {description}!')
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'lms/requestLeave.html')
