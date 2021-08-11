from django.shortcuts import render
from django.views import generic
from .forms import UserRegisterForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from leavemanagementsys.models import LeaveRequest


@login_required
def register(request):
    '''This is the signup page where 
    manager can create account for the new joinies'''
    if request.user.username == "admin":
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created {username}!')
                return HttpResponseRedirect(reverse('home'))
        else:
            form = UserRegisterForm()
        return render(request, 'users/signup.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('home'))


@login_required
def home(request):
    '''simple function to render the home page of LMS'''
    return render(request, 'users/home.html')


# @login_required
# def profile(request):
#     '''simple function to render the profile page of LMS
#     the leave list is printed in desc order of dates'''
#     data = LeaveRequest.objects.filter(
#         applied_user=request.user).order_by('-from_date')
#     return render(request, 'users/profile.html', {'datas': data})

class ViewListProfile(generic.ListView):
    model = LeaveRequest
    template_name = 'users/profile.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')
