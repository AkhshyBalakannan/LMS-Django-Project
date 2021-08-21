from django.views.generic import ListView, DetailView
from leavemanagementsys.models import LeaveRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from users.models import CustomUser
from .forms import LeaveCancelForm, LeaveRequestForm, LeaveRespondForm
from .leave_functionalities import date_range_exists, leave_respond, save_leave_form
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def request_leave(request):
    '''Request Leave'''
    form = LeaveRequestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if date_range_exists(form.cleaned_data['from_date'], form.cleaned_data['to_date'],
                                 request):
                return HttpResponseRedirect(reverse('home'))
            save_leave_form(form, request.user)
            messages.success(request, f'Leave requested Successfully!')
            return HttpResponseRedirect(reverse('home'))
        messages.warning(request, f'Invalid Entry!')
        return HttpResponseRedirect(reverse('leave-request'))
    return render(request, 'lms/requestLeave.html', {'form': form})


class ViewListCancelRequest(LoginRequiredMixin, ListView):
    '''List View for leave Cancel'''
    model = LeaveRequest
    template_name = 'lms/cancelLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        '''Get method'''
        return LeaveRequest.objects.filter(applied_user=self.request.user).order_by('-from_date')

    def post(self, form):
        form = LeaveCancelForm(self.request.POST)
        if form.is_valid():
            LeaveRequest.objects.filter(
                id=form.cleaned_data['id']).update(status='Cancel')
            messages.success(self.request, f'Leave cancelled!')
            return redirect('home')


class ViewListLeaveRequest(LoginRequiredMixin, ListView):
    '''List View for Leave Requests for manager'''
    model = LeaveRequest
    template_name = 'lms/list_respondLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        return LeaveRequest.objects.filter(
            applied_user__report_to=self.request.user).order_by('-from_date')


class ViewDetailLeaveRequest(LoginRequiredMixin, DetailView):
    '''Detailed View for leave Requests for manager'''
    model = LeaveRequest
    template_name = 'lms/detail_respondLeave.html'
    context_object_name = 'data'
    paginate_by = 5

    def post(self, request, pk):
        form = LeaveRespondForm(request.POST)
        if form.is_valid():
            leave_respond(form.cleaned_data, pk)
            messages.success(self.request, f"Leave Responded")
            return HttpResponseRedirect(reverse('list-leave-respond'))


class ViewListUserLeaves(LoginRequiredMixin, ListView):
    '''List view of leave made by user'''
    model = LeaveRequest
    template_name = 'lms/list_userLeave.html'
    context_object_name = 'datas'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,
                                 first_name=self.kwargs.get('user_first_name'))
        return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')
