import datetime
from dateutil import relativedelta
from django.contrib import messages
from leavemanagementsys.models import LeaveRequest
import pandas as pd
from .models import LeaveDates
from django.db.models import Sum


def save_leave_form(form, user):
    '''Save Leave Request with User detail'''
    leave = form.save(commit=False)
    leave.applied_user = user
    leave.save()


def date_validation(future_date):
    '''Date Validations Leave Request form'''
    validation_from_date = datetime.date.today()
    validation_to_date = validation_from_date+relativedelta.relativedelta(
        months=future_date)
    return validation_from_date, validation_to_date


def date_range_exists(from_date, to_date, request):
    '''Validation for leave existing'''
    to_store_dates = pd.date_range(from_date, to_date, freq='d').date
    count = 0
    for i in to_store_dates:
        dates, created = LeaveDates.objects.get_or_create(
            applied_user=request.user, dates=i)
        if not created:
            for i in to_store_dates:
                while count:
                    LeaveDates.objects.filter(dates=i).delete()
                    break
                count -= 1
            messages.warning(request, f'Leave already exists')
            return True
        count += 1


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
            'leave_count': leave_count, }


def leave_respond(form, leave_id):
    '''Respond Leave and backend work'''
    LeaveRequest.objects.filter(id=leave_id).update(
        remark=form['remark'], status=form['status'])
    leave = LeaveRequest.objects.filter(id=leave_id).first()
    user_with_leave = leave.applied_user
    leave = LeaveRequest.objects.filter(
        id=leave_id).filter(leave_type='personal', status='Approved').first()
    if leave:
        user_with_leave.leave_remaining -= int(leave.number_of_days)
        if user_with_leave.leave_remaining < 0:
            user_with_leave.leave_remaining = 0
            leave = LeaveRequest.objects.filter(
                id=leave_id).filter(leave_type='personal').update(leave_type='lop')
        user_with_leave.save()
