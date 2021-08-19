from django import forms
from leavemanagementsys.models import LeaveRequest
from .leave_functionalities import date_validation


class LeaveRequestForm(forms.ModelForm):
    min, max = date_validation(4)
    LEAVE_OPTIONS = (
        ('personal', 'Personal'),
        ('sick-covid', 'Sick-leave-Covid'),
    )
    from_date = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'min': min, 'max': max}))
    to_date = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'min': min, 'max': max}))
    leave_type = forms.ChoiceField(
        required=True, choices=LEAVE_OPTIONS)
    description = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'mt-1 mb-2', }))

    class Meta:
        model = LeaveRequest
        fields = ['from_date', 'to_date', 'leave_type', 'description']
        exclude = ['applied_user', 'status', 'remark', 'number_of_days']

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if not (from_date <= to_date or from_date <= self.min or to_date >= self.max):
            raise forms.ValidationError('Invalid form entry')


class LeaveCancelForm(forms.ModelForm):
    id = forms.IntegerField(required=True)

    class Meta:
        model = LeaveRequest
        fields = ['id', 'status']

    def clean(self):
        cleaned_data = super().clean()
        if not type(cleaned_data.get('id')) == int:
            raise forms.ValidationError('Invalid form entry')


class LeaveRespondForm(forms.ModelForm):
    OPTIONS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject'),
    )
    status = forms.ChoiceField(
        required=True, choices=OPTIONS)

    class Meta:
        model = LeaveRequest
        fields = ['remark', 'status']
