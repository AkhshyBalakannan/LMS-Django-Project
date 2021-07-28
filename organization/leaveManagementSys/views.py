from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import LeaveRequest
from django.views import View
from django.urls import reverse


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {'title': 'ABC HOME'})


class Signin(View):
    def get(self, request):
        return render(request, 'signin.html', {'title': 'Sign in'})

    def post(self, request):
        user = request.POST['userid']
        print(user)
        valid = get_object_or_404(User, username=user)
        if valid:
            return HttpResponseRedirect(reverse('employee-home', args=(valid.id,)))

        else:
            return Http404


class Employee(View):
    def get(self, request, pk):
        data = get_object_or_404(LeaveRequest, pk=pk)
        return render(request, 'employee_home.html', {'detail_data': data})

    def post(self, request, pk):
        leave = request.POST['reason']
        user = User.objects.filter(id=pk)
        leaverequest = LeaveRequest.objects.create(
            reason=leave, applied_user=User.objects.filter(id=pk),)
        leaverequest.save()
        return HttpResponseRedirect(reverse('employee-home', args=(pk,)))


def list_lms_admin(request):
    list_data = {'details': LeaveRequest.objects.all()}
    return render(request, 'admin_list.html', list_data)


def detailed_lms_admin(request, pk):
    detail_data = get_object_or_404(LeaveRequest, pk=pk)
    return render(request, 'admin_detail.html', {'detail_data': detail_data, })
