from django import forms
from django.forms import ModelForm
from .models import LeaveType, LeaveRequest

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveTypeForm(ModelForm):
    class Meta:
        model = LeaveType
        fields = ['leave_type', 'detail']

    def __init__(self, *args, **kwargs):
        super(LeaveTypeForm, self).__init__(*args, **kwargs)
        self.fields['leave_type'].widget.attrs['placeholder'] = 'Enter the Leave Type:'
        self.fields['detail'].widget.attrs['placeholder'] = 'Enter the detail of the Leave Type:'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class LeaveRequestForm(ModelForm):
    booking_date = forms.DateField(widget=DateInput)
    class Meta:
        model = LeaveRequest
        fields = ('title', 'detail', 'from_date', 'to_date', 'leave_type')
        labels = {
            'title': '',
            'detail': '',
            'from_date': '',
            'to_date': '',
            'leave_type': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Title'}),
            'detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the detail'}),
            'from_date': forms.TextInput(attrs={'class': 'form-control', 'name': 'from_date', 'id': 'date'}),
            'to_date': forms.TextInput(attrs={'class': 'form-control', 'name': 'date'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            
        }