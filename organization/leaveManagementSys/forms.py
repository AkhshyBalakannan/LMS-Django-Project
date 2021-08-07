from django import forms
from django.forms.models import ModelForm
from leavemanagementsys.models import LeaveRequest


class LeaveRequestForm(ModelForm):
    OPTIONS = (
        ('Personal', 'Personal'),
        ('Covid_permission', 'Covid_permission'),
    )
    description = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'mt-1 mb-2', }))
    from_date = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'min': '{{ today }}', 'max': "{{ year_duration }}-{{ month_duration }}-{{ day_duration }}"}))
    to_date = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'min': '{{ today }}', 'max': "{{ year_duration }}-{{ month_duration }}-{{ day_duration }}"}))
    leave_type = forms.ChoiceField(
        required=True, choices=OPTIONS)

    class Meta:
        model = LeaveRequest
        fields = ['from_date', 'to_date', 'leave_type', 'description']
