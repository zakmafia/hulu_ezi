from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Priority, Role, Staff, Issue, UserRequest, KnowledgeBase, Ticket


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a priority'})
        }

class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a role'})
        }

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['member', 'role']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['name', 'priority', 'assigned_to']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter the issue'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'})
        }

class UserRequestForm(ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = UserRequest
        fields = ['issue', 'is_other_issue' ,'other_issue', 'issue_description', 'image']
        widgets = {
            'issue': forms.Select(attrs={'class': 'form-control', 'name': 'issue', 'id': 'issue'}),
            'is_other_issue': forms.CheckboxInput(attrs={'name': 'is_other_issue', 'id': 'is_other_issue'}),
            'other_issue': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter the issue', 'disabled': True, 'name': 'other_issue', 'id': 'other_issue'}),
            'issue_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the issue description'}),
        }
    
    def clean(self):
        if self.cleaned_data['issue'] is None and self.cleaned_data['is_other_issue'] == False:
            raise ValidationError('You should select an issue or fill the other issue')
        if self.cleaned_data['is_other_issue'] == True and self.cleaned_data['other_issue'] == "":
            raise ValidationError('You should fill the other issue')

class TicketForm(ModelForm, forms.Form):
    allocated_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    deadline = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    completion_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker'}), required=False)
    class Meta:
        model = Ticket
        fields = ['task', 'priority', 'assigned_person', 'allocated_date', 'deadline', 'weight', 'status', 'completion_date']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the task'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_person': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class KnowledgeBaseForm(forms.Form, ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    class Meta:
        model = KnowledgeBase
        fields = ['docfile', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }