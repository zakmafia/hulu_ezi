from django import forms
from django.forms import ModelForm
from .models import Booking, Room

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

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

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'from_date', 'to_date', 'from_time', 'to_time', 'description']
        widgets = {
            'from_date': DateInput(attrs={'name': 'from_date'}),
            'to_date': DateInput(attrs={'name': 'to_date'}),
            'from_time': TimeInput(),
            'to_time': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name of the meeting'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter the meeting detail'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

