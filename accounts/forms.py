from django import forms
from .models import Account
from .utils import validate_email_string

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        email_data = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email_domain_string = email_data.split('@')[0]
        email_domain = email_data.split('@')[1]
        email_domain_list = ["hst-et.com"]
        if email_domain not in email_domain_list:
            raise forms.ValidationError(
                "Email is not in the HST Domain!"
            )

        if not validate_email_string(email_domain_string):
            raise forms.ValidationError(
                "Email is not in the HST Domain!"
            )

        
        if not validate_email_string(email_domain_string):
            raise forms.ValidationError(
                "Not a Valid HST email for registeration!"
            )

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
