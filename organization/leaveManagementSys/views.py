import datetime
from django.views import generic
from leavemanagementsys.models import LeaveRequest, LeaveDates
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from users.models import CustomUser
from django.db import IntegrityError
from .forms import LeaveRequestForm, LeaveRespondForm


@login_required
def request_leave(request):
    '''Request leave functions where employee or manager 
    can request leave for themselves 
    employee leave are kept pending
    manager leave are approved immediately'''
    # datetime.date will give us date date variable alone
    validation_from_date = datetime.date.today()
    # Custom form imported from .forms and given
    # request.POST will have the form data
    form = LeaveRequestForm(request.POST or None)
    logged_user = request.user
    if request.method == 'POST':
        if form.is_valid():  # to validate form
            # validated data are present inside cleaned_data dict type
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            leave_type = form.cleaned_data['leave_type']
            description = form.cleaned_data['description']
            # Number of days are calculated by from and to date
            if from_date.month == to_date.month:
                if from_date.day > to_date.day:
                    # to check from date is not less than to date
                    messages.warning(
                        request, f'Your trying an invalid form entry')
                    return HttpResponseRedirect(reverse('leave-request'))
                # Simple sub add method if same month
                number_of_days = to_date.day - from_date.day + 1
            else:
                if from_date.month > to_date.month:
                    # to check from date is not less than to date
                    messages.warning(
                        request, f'Your trying an invalid form entry')
                    return HttpResponseRedirect(reverse('leave-request'))
                # if different month check which month
                # this extra check is for calculating
                # number of days in month
                calculate_number_of_days = to_date.day
                if from_date.month in [4, 6, 9, 11]:
                    calculate_number_of_days += 30
                else:
                    calculate_number_of_days += 31
                number_of_days = calculate_number_of_days - from_date.day + 1

            # past from_date validation in server side
            if validation_from_date.year >= from_date.year and validation_from_date.month >= from_date.month and validation_from_date.day > from_date.day:
                messages.warning(
                    request, f'Leave Request cannot be made to past dates')
                return HttpResponseRedirect(reverse('leave-request'))

             # past to date validation in server side
            if validation_from_date.year >= to_date.year and validation_from_date.month >= to_date.month and validation_from_date.day > to_date.day:
                messages.warning(
                    request, f'Leave Request cannot be made to past dates')
                return HttpResponseRedirect(reverse('leave-request'))

            try:
                # getting leavedates for signed user
                leave_dates = LeaveDates.objects.filter(
                    applied_user=request.user)
                for leave_date in leave_dates:
                    # faster check given dates are present in leavedates
                    if str(leave_date) == str(from_date) or str(leave_date) == str(to_date):
                        raise IntegrityError
                    to_check_date = number_of_days
                    date = from_date
                    # To faster the performance we check no of days
                    if not to_check_date == 1:
                        while to_check_date:
                            if str(leave_date) == str(date):
                                raise IntegrityError
                            # this is to increment date to check in loop
                            date = date+datetime.timedelta(days=1)
                            # the above set is done for period of leave request
                            to_check_date -= 1
                if leave_type == 'Covid_permission':
                    # free leave for covid permission is 7 days
                    if int(number_of_days) > 7:
                        messages.warning(
                            request, f'Covid Leave span is only 7 days')
                        return HttpResponseRedirect(reverse('leave-request'))
                # If all above validations are passed than
                # leave request is created with leave dates inserted in table
                LeaveRequest.objects.create(applied_user=request.user,
                                            description=description, from_date=from_date, to_date=to_date, leave_type=leave_type, number_of_days=number_of_days)
               # the below code is to store the period of leave dates
                to_store_date = number_of_days
                date = from_date
                while to_store_date:
                    # creating leave dates in leavedates table
                    LeaveDates.objects.create(
                        applied_user=request.user, dates=date)
                    date = date+datetime.timedelta(days=1)
                    to_store_date -= 1
                # Validating whether its manager to approve leave
                if request.user.is_manager:
                    ''' Updates entry as approved if its manager'''
                    LeaveRequest.objects.update(status="Approved")
                    if not leave_type == 'Covid_permission':
                        # To increment the leave dates taken by user
                        logged_user.leave_taken += int(number_of_days)
                        logged_user.leave_remaining -= int(number_of_days)
                        if logged_user.leave_remaining < 0:
                            # once leave remaining are over LOP are calculated
                            number_of_days = -int(logged_user.leave_remaining)
                            logged_user.leave_remaining = 0
                            logged_user.lop_leave_taken += int(number_of_days)
                            logged_user.leave_type = 'LOP_leave'
                        # save the data in user has this is not build-in method
                    logged_user.save()
                # to calculate covid leave
                if leave_type == 'Covid_permission':
                    logged_user.covid_leave_taken += int(number_of_days)
                    logged_user.save()
                    messages.success(
                        request, f'Take care of your health')

                messages.success(
                    request, f'Leave Request Successfully submitted !')
                return HttpResponseRedirect(reverse('home'))

            except IntegrityError:
                # Exceptions meaning unique column values
                # we dont have unique tables constraints but
                # we use the name and raise error by ourselves
                messages.warning(
                    request, f'Leave Request For the day already exists')
                return HttpResponseRedirect(reverse('home'))
        else:
            # This will work after the try block happens
            return HttpResponseRedirect(reverse('leave-request'))
    else:
        # This block of code is for GET method
        # with some user side validations form
        advanced_month_range = 4
        validation_to_day = validation_from_date.day
        validation_to_year = validation_from_date.year
        validation_to_month = validation_from_date.month+advanced_month_range
        while validation_to_month > 12:
            # which loop runs when to year is next year
            validation_to_year += 1
            validation_to_month -= 12
        if validation_to_day <= 9:
            # this is done to make it double digit
            # If not done than html validations wont work
            validation_to_day = f'0{validation_to_day}'
        if validation_to_month <= 9:
            # this is done to make it double digit
            # If not done than html validations wont work
            validation_to_month = f'0{validation_to_month}'
        # return the html with data given as dict form
        return render(request, 'lms/requestLeave.html',
                      {'form': form, 'today': str(validation_from_date),
                       'month_duration': validation_to_month,
                       'year_duration': validation_to_year,
                       'day_duration': validation_to_day})


@login_required
def cancel_request(request):
    '''This is the leave cancel function'''
    if request.method == 'POST':
        data = request.POST  # all data in post are collected
        if data.get('id') == '':
            # validate server side the data received
            messages.warning(
                request, f'Your trying an invalid form entry')
            return HttpResponseRedirect(reverse('cancel-request'))
        leave_id = data.get('id')
        # getting the leaverequest from database
        data = LeaveRequest.objects.filter(
            applied_user=request.user, id=leave_id)
        # Updating leaverequest as cancel
        data.update(status="Cancel")
        messages.success(
            request, f'Leave Request Successfully cancelled!')
        return HttpResponseRedirect(reverse('home'))
    else:
        # This is GET method
        data = LeaveRequest.objects.filter(
            applied_user=request.user).order_by('-from_date')
        return render(request, 'lms/cancelLeave.html', {'datas': data})


class ViewListLeaveRequest(generic.ListView):
    '''This is manager accessable page to view 
    list of leave request'''
    model = LeaveRequest
    template_name = 'lms/list_respondLeave.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    ordering = ['-from_date']
    paginate_by = 5


class ViewDetailLeaveRequest(generic.DetailView):
    '''This is manager accessable page to view 
    detail view of request matched with get route 
    This is easily done using the pk value in url'''
    model = LeaveRequest
    template_name = 'lms/detail_respondLeave.html'
    context_object_name = 'data'


class ViewListUserLeaves(generic.ListView):
    '''This is manager accessable page to view 
    list of leave request done by the particular user'''
    model = LeaveRequest
    template_name = 'lms/list_userLeave.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    paginate_by = 5

    def get_queryset(self):
        # here the data is gathered
        # from database using build-in method get_object_or_404
        # which automatically gives us a 404 status
        user = get_object_or_404(
            CustomUser, first_name=self.kwargs.get('user_first_name'))
        return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')


@login_required
def leave_request_process(request, pk):
    '''This is one way function where only POST
    method is happened and GET method is not supported'''
    if request.method == 'POST':
        # User written form is given with the data from method.POST
        form = LeaveRespondForm(request.POST)
        if form.is_valid():
            # validated data are stored in variables
            remark = form.cleaned_data['remark']
            status = form.cleaned_data['status']
            # leaverequest data is taken from database
            leave = LeaveRequest.objects.get(id=pk)
            # Taken leaverequest data is updated with remark and status
            LeaveRequest.objects.filter(id=pk).update(
                remark=remark, status=status)
            # below code is to increment the number of leavetaken
            # of user who applied leave with respected number of dates
            if status == "Approved" and not leave.leave_type == 'Covid_permission':
                # This if statement is exicuted only when
                # status is approved and the leave type
                # is not Covid_permissions
                user_with_leave = leave.applied_user
                number_of_days = leave.number_of_days
                user_with_leave.leave_taken += int(number_of_days)
                user_with_leave.leave_remaining -= int(number_of_days)
                if user_with_leave.leave_remaining < 0:
                    # once leave remaining are over LOP are calculated
                    number_of_days = -int(user_with_leave.leave_remaining)
                    user_with_leave.leave_remaining = 0
                    user_with_leave.lop_leave_taken += int(number_of_days)
                    user_with_leave.leave_type = 'LOP_leave'
                # save the data in user has this is not build-in method
                user_with_leave.save()
                messages.success(
                    request, f'Leave Request has been Approved :)')
            elif status == "Reject":
                # if the leave is rejected just a message is done
                messages.warning(
                    request, f"Leave Request has been Rejected :'(")
            return HttpResponseRedirect(reverse('list-leave-respond'))
        else:
            '''if the form is not valid user trying spam server'''
            messages.warning(
                request, f"Your trying an invalid form entry")
            return HttpResponseRedirect(reverse('list-leave-respond'))
