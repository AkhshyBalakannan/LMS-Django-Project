'''Custom User forms create/update form'''
from django import forms
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Select
from users.models import CustomUser

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class UserRegisterForm(UserCreationForm):
    '''Custom User registeration form'''
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    report_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_manager=True), required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1',
                  'password2', 'profile_pic', 'address', 'is_manager', 'report_to', ]


class UserSelectUpdateForm(ModelForm):
    '''Get instance of users'''
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email']


class UserUpdationForm(ModelForm):
    '''Updation form for custom user'''
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    report_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_manager=True), required=True, empty_label=None)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number',
                  'address', 'is_manager', 'report_to', ]
