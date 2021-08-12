from django.contrib.auth.models import UserManager
from users.models import CustomUser
from django.shortcuts import redirect, render
from django.views import generic
from .forms import UserRegisterForm, UserSelectUpdateForm, UserUpdationForm
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from leavemanagementsys.models import LeaveRequest
from django.db import DataError


@login_required
def register(request):
    '''This is the signup page where 
    admin can create account for the new joinies'''
    if request.user.is_admin_employee == True:    # validation for checking is_admin
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)   # django validating form
            if form.is_valid():  # checking is it valid
                form.save()
                # Cleaned_data will contain data after validations
                username = form.cleaned_data.get('username')
                # message is from django where the base template has if message statement
                messages.success(request, f'Account created {username}!')
                return HttpResponseRedirect(reverse('home'))
        else:   # if method is GET then empty form is given for rendering
            form = UserRegisterForm()
        return render(request, 'users/signup.html', {'form': form})
    else:
        # This is an extra step of validating that only admin can access
        # other users are redirected to home screen
        return HttpResponseRedirect(reverse('home'))


@login_required
def select_update_user(request):
    '''This is the user name select for updation view'''
    if request.user.is_admin_employee == True:    # validation for checking is_admin
        form = UserSelectUpdateForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():  # checking is it valid
                email = form.cleaned_data['email']
                return HttpResponseRedirect(reverse('update-user', kwargs={'email': email}))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'users/update_user.html', {'form': form})
    else:
        # This is an extra step of validating that only admin can access
        # other users are redirected to home screen
        return HttpResponseRedirect(reverse('home'))


@login_required
def update_user(request, email):
    '''This is the signup page where 
    admin can update account for the new joinies'''
    if request.user.is_admin_employee == True:    # validation for checking is_admin
        # django validating form
        if request.method == 'POST':
            try:
                form = request.POST
                username = form['username']
                if request.POST.get('is_admin_employee', False) == 'on':
                    is_admin_employee = True
                else:
                    is_admin_employee = False
                if request.POST.get('is_employee', True) == 'on':
                    is_employee = True
                else:
                    is_employee = False
                if request.POST.get('is_manager', False) == 'on':
                    is_manager = True
                else:
                    is_manager = False
                CustomUser.objects.filter(
                    username=username).update(email=form['email'], first_name=form['first_name'],
                                              last_name=form['last_name'], phone_number=form['phone_number'],
                                              profile_pic=form['profile_pic'], address=form['address'],
                                              is_admin_employee=is_admin_employee,
                                              is_employee=is_employee, is_manager=is_manager,
                                              leave_eligible=form['leave_eligible'], leave_taken=form['leave_taken'],
                                              leave_remaining=form['leave_remaining'],
                                              lop_leave_taken=form['lop_leave_taken'],
                                              covid_leave_taken=form['covid_leave_taken'])
                # Cleaned_data will contain data after validations
                username = form['username']
                # message is from django where the base template has if message statement
                messages.success(
                    request, f'Account updated for username {username}!')
                return HttpResponseRedirect(reverse('home'))
            except DataError:
                messages.warning(
                    request, f'Your trying an invalid form data mostly mobile number is incorrect')
                return HttpResponseRedirect(reverse('home'))
        else:   # if method is GET then empty form is given for rendering
            update_user = CustomUser.objects.filter(email=email).first()
            print(update_user)
            if update_user == None:
                messages.warning(
                    request, f'No matching email Id were found in database Please check the mail Id entered')
                return HttpResponseRedirect(reverse('home'))
            return render(request, 'users/update_user_submit.html', {'update_user': update_user})
    else:
        # This is an extra step of validating that only admin can access
        # other users are redirected to home screen
        return HttpResponseRedirect(reverse('home'))


@login_required
def home(request):
    '''simple function to render the home page of LMS'''
    return render(request, 'users/home.html')


@login_required
def user_profile(request):
    '''simple function to render the user profile page of user'''
    return render(request, 'users/user_profile.html')


class ViewListProfile(generic.ListView):
    '''This is profile class where the leave data of 
    particular signed in user leave can be viewed'''
    model = LeaveRequest    # telling django the model it has to look for
    template_name = 'users/profile.html'    # Explicit allocating temp
    context_object_name = 'datas'   # Explicit allocating var name
    paginate_by = 5

    def get_queryset(self):
        '''Queryset is the function we write to 
        tell django what we need it to return for us'''
        user = self.request.user    # Here all data can be accessed using self keyword
        return LeaveRequest.objects.filter(applied_user=user).order_by('-from_date')
