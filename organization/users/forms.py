from django.forms.models import ModelForm
from users.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


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
    report_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_manager=True), required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number',
                  'address', 'is_manager', 'report_to', ]
