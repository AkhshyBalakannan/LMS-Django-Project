'''Views module for leave management sys app'''
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from users.models import CustomUser
from leavemanagementsys.models import LeaveRequest
from .forms import LeaveCancelForm, LeaveRequestForm, LeaveRespondForm
from .leave_functionalities import (date_range_exists, leave_respond,
                                    list_cancel_leave, leave_form_save)


# pylint: disable=too-many-ancestors

@login_required
def request_leave(request):
    '''Request Leave'''
    form = LeaveRequestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if date_range_exists(form.cleaned_data['from_date'], form.cleaned_data['to_date'],
                                 request):
                return HttpResponseRedirect(reverse('home'))
            leave_form_save(form, request.user)
            messages.success(request, 'Leave requested Successfully!')
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'lms/requestLeave.html', {'form': form}, status=400)
    return render(request, 'lms/requestLeave.html', {'form': form})


class ViewListCancelRequest(LoginRequiredMixin, ListView):
    '''List View for leave Cancel'''
    model = LeaveRequest
    template_name = 'lms/cancelLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        '''Get method'''
        return list_cancel_leave(self.request.user)

    def post(self, form):
        '''Post Method'''
        form = LeaveCancelForm(self.request.POST)
        if form.is_valid():
            LeaveRequest.objects.filter(
                id=form.cleaned_data['id']).update(status='Cancel')
            messages.success(self.request, 'Leave cancelled!')
            return redirect('home')
        messages.warning(self.request, 'Invalid try')
        return list_cancel_leave(self.request.user)


class ViewListLeaveRequest(LoginRequiredMixin, ListView):
    '''List View for Leave Requests for manager'''
    model = LeaveRequest
    template_name = 'lms/list_respondLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        return LeaveRequest.objects.filter(applied_user__report_to=self.request.user).order_by('-from_date')


class ViewDetailLeaveRequest(LoginRequiredMixin, DetailView):
    '''Detailed View for leave Requests for manager'''
    model = LeaveRequest
    template_name = 'lms/detail_respondLeave.html'
    context_object_name = 'data'
    paginate_by = 5

    def post(self, request, pk):  # pylint: disable=invalid-name
        '''Post Method'''
        form = LeaveRespondForm(request.POST)
        if form.is_valid():
            leave_respond(form.cleaned_data, pk)
            messages.success(self.request, 'Leave Responded')
            return HttpResponseRedirect(reverse('list-leave-respond'))
        return HttpResponseRedirect(reverse('detail-leave-respond'))


class ViewListUserLeaves(LoginRequiredMixin, ListView):
    '''List view of leave made by user'''
    model = LeaveRequest
    template_name = 'lms/list_userLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,
                                 first_name=self.kwargs.get('user_first_name'))
        if user:
            return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')


@login_required
def search_employee(request):
    '''search employee'''
    if request.method == 'POST':
        employee = CustomUser.objects.filter(
            email=request.POST.get('employee_email')).first()
        if employee == None:
            messages.warning(request, "No User Found")
            return render(request, 'lms/search_employee.html', {'title': 'Search Employee'}, status=404)
        elif request.user.groups.filter(name='Adminstrator').exists() or not employee.is_manager:
            return redirect('employee-leaves', request.POST.get('employee_email'))
        messages.warning(request, "You have no permission")
        return render(request, 'lms/search_employee.html', {'title': 'Search Employee'}, status=401)
    return render(request, 'lms/search_employee.html', {'title': 'Search Employee'})


class ViewListEmployeeLeaves(LoginRequiredMixin, ListView):
    '''List view of leave made by user'''
    model = LeaveRequest
    template_name = 'lms/employee_leave_details.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,
                                 email=self.kwargs.get('user_email_id'))
        if user:
            return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')
