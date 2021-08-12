from django.forms.models import ModelForm
from users.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2',
                  'profile_pic', 'address', 'is_admin_employee', 'is_employee', 'is_manager', 'leave_eligible',
                  'leave_taken', 'leave_remaining', 'lop_leave_taken',
                  'covid_leave_taken']


class UserSelectUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']


class UserUpdationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number',
                  'profile_pic', 'address', 'is_admin_employee', 'is_employee', 'is_manager', 'leave_eligible',
                  'leave_taken', 'leave_remaining', 'lop_leave_taken',
                  'covid_leave_taken']
