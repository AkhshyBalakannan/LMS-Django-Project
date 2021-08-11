import datetime
from django.db.models.fields import IntegerField
from django.urls.base import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView
from leavemanagementsys.models import LeaveRequest, LeaveDates
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from users.models import CustomUser
from django.db import IntegrityError
from .forms import LeaveRequestForm, LeaveRespondForm


@login_required
def request_leave(request):
    '''This is an request leave functions where employee
    or manager can request or say as register leave for themselves'''
    validation_from_date = datetime.date.today()
    form = LeaveRequestForm(request.POST or None)
    logged_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            leave_type = form.cleaned_data['leave_type']
            description = form.cleaned_data['description']
            number_of_days = to_date.day - from_date.day + 1

            if validation_from_date.year >= from_date.year and validation_from_date.month >= from_date.month and validation_from_date.day > from_date.day:
                messages.warning(
                    request, f'Leave Request cannot be made to past dates')
                return HttpResponseRedirect(reverse('leave-request'))

            if validation_from_date.year >= to_date.year and validation_from_date.month >= to_date.month and validation_from_date.day > to_date.day:
                messages.warning(
                    request, f'Leave Request cannot be made to past dates')
                return HttpResponseRedirect(reverse('leave-request'))

            try:
                leave_dates = LeaveDates.objects.filter(
                    applied_user=request.user)
                print(leave_dates)
                for leave_date in leave_dates:
                    if str(leave_date) == str(from_date) or str(leave_date) == str(to_date):
                        print('from if ')
                        raise IntegrityError
                    to_check_date = number_of_days
                    date = from_date
                    if not to_check_date == 1:
                        while to_check_date:
                            if str(leave_date) == str(date):
                                print("hey from while")
                                raise IntegrityError
                            date = date+datetime.timedelta(days=1)
                            to_check_date -= 1
                print("before if covid")
                if leave_type == 'Covid_permission':
                    if int(number_of_days) > 7:
                        messages.warning(
                            request, f'Covid Leave span is only 7 days')
                        return HttpResponseRedirect(reverse('leave-request'))
                print("Before creations of leave")
                LeaveRequest.objects.create(applied_user=request.user,
                                            description=description, from_date=from_date, to_date=to_date, leave_type=leave_type, number_of_days=number_of_days)
                print("after Creation of leave")
                to_store_date = number_of_days
                date = from_date
                while to_store_date:
                    LeaveDates.objects.create(
                        applied_user=request.user, dates=date)
                    date = date+datetime.timedelta(days=1)
                    to_store_date -= 1

                if request.user.is_manager:
                    ''' Updates all entry as approved if its manager'''
                    LeaveRequest.objects.update(status="Approved")
                    logged_user.leave_taken += int(number_of_days)
                    logged_user.leave_remaining -= int(number_of_days)
                    if logged_user.leave_remaining < 0:
                        number_of_days = -int(logged_user.leave_remaining)
                        logged_user.leave_remaining = 0
                        logged_user.lop_leave_taken += int(number_of_days)
                        logged_user.leave_type = 'LOP_leave'
                    logged_user.save()

                if leave_type == 'Covid_permission':
                    logged_user.covid_leave_taken += int(number_of_days)
                    logged_user.save()
                    messages.success(
                        request, f'Take care of your health')

                messages.success(
                    request, f'Leave Request Successfully submitted !')
                return HttpResponseRedirect(reverse('home'))

            except IntegrityError:
                messages.warning(
                    request, f'Leave Request For the day already exists')
                return HttpResponseRedirect(reverse('home'))
        else:
            print(form)
            return HttpResponseRedirect(reverse('leave-request'))
    else:
        advanced_month_range = 4
        validation_to_day = validation_from_date.day
        validation_to_year = validation_from_date.year
        validation_to_month = validation_from_date.month+advanced_month_range
        while validation_to_month > 12:
            validation_to_year += 1
            validation_to_month -= 12
        if validation_to_day <= 9:
            validation_to_day = f'0{validation_to_day}'
        if validation_to_month <= 9:
            validation_to_month = f'0{validation_to_month}'
        return render(request, 'lms/requestLeave.html',
                      {'form': form, 'today': str(validation_from_date),
                       'month_duration': validation_to_month,
                       'year_duration': validation_to_year,
                       'day_duration': validation_to_day})


@login_required
def cancel_request(request):
    '''This is the leave cancel function'''
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
    '''This is manager page to view list of request'''
    model = LeaveRequest
    template_name = 'lms/list_respondLeave.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    ordering = ['-from_date']
    paginate_by = 5


class ViewDetailLeaveRequest(generic.DetailView):
    '''This is manager page to view detail view of request matched with get route'''
    model = LeaveRequest
    template_name = 'lms/detail_respondLeave.html'
    context_object_name = 'data'


class ViewListUserLeaves(generic.ListView):
    '''This is manager page to view list of request'''
    model = LeaveRequest
    template_name = 'lms/list_userLeave.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            CustomUser, first_name=self.kwargs.get('user_first_name'))
        return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')


@login_required
def leave_request_process(request, pk):
    if request.method == 'POST':
        form = LeaveRespondForm(request.POST)
        if form.is_valid():
            remark = form.cleaned_data['remark']
            status = form.cleaned_data['status']
            leave = LeaveRequest.objects.get(id=pk)
            LeaveRequest.objects.filter(id=pk).update(
                remark=remark, status=status)
            if status == "Approved" and not leave.leave_type == 'Covid_permission':
                user_with_leave = leave.applied_user
                number_of_days = leave.number_of_days
                user_with_leave.leave_taken += int(number_of_days)
                user_with_leave.leave_remaining -= int(number_of_days)
                if user_with_leave.leave_remaining < 0:
                    number_of_days = -int(user_with_leave.leave_remaining)
                    user_with_leave.leave_remaining = 0
                    user_with_leave.lop_leave_taken += int(number_of_days)
                    user_with_leave.leave_type = 'LOP_leave'
                user_with_leave.save()
                messages.success(
                    request, f'Leave Request has been Approved :)')
            elif status == "Reject":
                messages.warning(
                    request, f"Leave Request has been Rejected :'(")
            return HttpResponseRedirect(reverse('list-leave-respond'))
