'''Leave related Functions called from views forms'''
import datetime
from dateutil import relativedelta
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def paginator_function(request):
    '''Leave Profile paginator for FBViews'''
    datas = LeaveRequest.objects.filter(applied_user=request.user
                                        ).order_by('-from_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(datas, 5)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    finally:
        return datas


def leave_details(request, user):
    '''Leave Profile with leave details'''
    datas = paginator_function(request)
    leave_count = user.leaverequest_set.filter(
        status="Approved").aggregate(total=Sum('number_of_days'))
    personal_leave = user.leaverequest_set.filter(
        leave_type="personal", status="Approved").aggregate(total=Sum('number_of_days'))
    lop_count = user.leaverequest_set.filter(
        status="Approved", leave_type='lop').aggregate(total=Sum('number_of_days'))
    other_leave_count = user.leaverequest_set.filter(status="Approved").exclude(
        leave_type__in=['personal', 'lop']).aggregate(total=Sum('number_of_days'))
    return {'datas': datas, 'lop_count': lop_count,
            'other_leave_count': other_leave_count,
            'leave_count': leave_count,
            'personal_leave': personal_leave,
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
        cal_lop = user_with_leave.leave_remaining - int(leave.number_of_days)
        if user_with_leave.leave_remaining == 0:
            LeaveRequest.objects.filter(
                id=leave_id).update(leave_type='lop')
        elif cal_lop < 0:
            split_leave(leave)
            user_with_leave.leave_remaining = 0
        else:
            user_with_leave.leave_remaining -= int(leave.number_of_days)
        user_with_leave.save()


def split_leave(leave):
    '''Split leave for LOP leave type'''
    user_with_leave = leave.applied_user
    personal_leave_count = user_with_leave.leave_remaining
    cal_to_date = leave.from_date+relativedelta.relativedelta(
        days=personal_leave_count-1)
    cal_from_date = leave.from_date+relativedelta.relativedelta(
        days=personal_leave_count)
    LeaveRequest.objects.create(applied_user=user_with_leave, description=leave.description, from_date=leave.from_date,
                                to_date=cal_to_date, leave_type='personal', status=leave.status, remark=leave.remark)
    LeaveRequest.objects.create(applied_user=user_with_leave, description=leave.description, from_date=cal_from_date,
                                to_date=leave.to_date, leave_type='lop', status=leave.status, remark=leave.remark)
    leave.delete()
