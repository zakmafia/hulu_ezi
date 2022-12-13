from django import forms
from django.forms import ModelForm
from .models import Booking, Room, AvailableTime

class DateInput(forms.DateInput):
    input_type = 'date'


class RoomForm(ModelForm):
    images = forms.ImageField()
    class Meta:
        model = Room
        fields = ['name', 'address', 'images']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the room name'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter the room address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class AvailableTimeForm(ModelForm):
    class Meta:
        model = AvailableTime
        fields = ('available_time',)
        labels ={
            'available_time': ''
        }
        widgets = {
            'available_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the available times'})
        }