'''Leave related Functions called from views forms'''
import datetime
from dateutil import relativedelta
from django.contrib import messages
from django.db.models import Sum
import pandas as pd
from leavemanagementsys.models import LeaveRequest
from .models import LeaveDates


# pylint: disable=no-member
# pylint: disable=unused-variable


def leave_form_save(form, user):
    '''Save Leave Request with User detail'''
    leave = form.save(commit=False)
    leave.applied_user = user
    leave.save()


def list_cancel_leave(user):
    '''Cancel Leave request list'''
    return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')


def date_validation(future_date):
    '''Date Validations Leave Request form'''
    validation_from_date = datetime.date.today()
    validation_to_date = validation_from_date+relativedelta.relativedelta(
        months=future_date)
    return validation_from_date, validation_to_date


def leave_details(user):
    '''Leave Profile with leave details'''
    datas = LeaveRequest.objects.filter(applied_user=user
                                        ).order_by('-from_date')
    leave_count = user.leaverequest_set.filter(
        status="Approved", leave_type='personal').aggregate(total=Sum('number_of_days'))
    lop_count = user.leaverequest_set.filter(
        status="Approved", leave_type='lop').aggregate(total=Sum('number_of_days'))
    other_leave_count = user.leaverequest_set.filter(status="Approved").exclude(
        leave_type__in=['personal', 'lop']).aggregate(total=Sum('number_of_days'))
    return {'datas': datas, 'lop_count': lop_count,
            'other_leave_count': other_leave_count,
            'leave_count': leave_count,
            'title': 'Leave Profile'}


def date_range_exists(from_date, to_date, request):
    '''Validation for leave existing'''
    to_store_dates = pd.date_range(from_date, to_date, freq='d')
    count = 0
    for store_date in to_store_dates:
        dates, created = LeaveDates.objects.get_or_create(
            applied_user=request.user, dates=store_date)
        if not created:
            for exist_date in to_store_dates:
                while count:
                    LeaveDates.objects.filter(
                        dates=exist_date).delete()
                    break
                count -= 1
            messages.warning(request, 'Leave already exists')
            return True
        count += 1
    return False


def leave_respond(form, leave_id):
    '''Respond Leave and backend work'''
    LeaveRequest.objects.filter(id=leave_id).update(
        remark=form['remark'], status=form['status'])
    leave = LeaveRequest.objects.filter(
        id=leave_id).first()
    user_with_leave = leave.applied_user
    leave = LeaveRequest.objects.filter(
        id=leave_id, leave_type='personal', status='Approved').first()
    if leave:
        user_with_leave.leave_remaining -= int(leave.number_of_days)
        if user_with_leave.leave_remaining < 0:
            user_with_leave.leave_remaining = 0
            leave = LeaveRequest.objects.filter(
                id=leave_id, leave_type='personal').update(leave_type='lop')
        user_with_leave.save()
