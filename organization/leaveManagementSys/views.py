from django.urls.base import reverse_lazy
from django.views import generic
from typing import Generic

from django.views.generic.edit import UpdateView
from leavemanagementsys.models import LeaveRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView


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
        logged_user.leave_remaining -= int(number_of_days)
        if logged_user.leave_remaining < 0:
            number_of_days = -int(logged_user.leave_remaining)
            logged_user.leave_remaining = 0
            logged_user.lop_leave_taken += int(number_of_days)
        logged_user.save()
        messages.success(
            request, f'Leave Request Successfully submitted for {description}!')
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'lms/requestLeave.html')


@login_required
def cancel_request(request):
    if request.method == 'POST':
        data = request.POST
        leave_id = data.get('id')
        data = LeaveRequest.objects.filter(
            applied_user=request.user, id=leave_id)
        data.update(status="Cancel")
        messages.success(
            request, f'Leave Request Successfully cancelled!')
        return HttpResponseRedirect(reverse('home'))
    else:
        data = LeaveRequest.objects.filter(
            applied_user=request.user).order_by('-from_date')
        return render(request, 'lms/cancelLeave.html', {'datas': data})


class ViewListLeaveRequest(generic.ListView):
    template_name = 'lms/list_respondLeave.html'
    context_object_name = 'datas'

    def get_queryset(self):
        return LeaveRequest.objects.all()


class ViewDetailLeaveRequest(generic.DetailView):
    model = LeaveRequest
    template_name = 'lms/detail_respondLeave.html'
    context_object_name = 'data'


class LeaveRequestUpdate(UpdateView):
    model = LeaveRequest
    fields = ['remark', 'status']
    # success_url = '/leaveRespond/'
    success_url = reverse_lazy('list-leave-respond')
                                                                