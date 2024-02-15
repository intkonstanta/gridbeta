from django.forms import ModelForm, TextInput, DateInput, NumberInput , FileInput
from django import forms
from .models import *
import datetime

class CreateProjectForm(ModelForm):
    class Meta:
        model = user_project
        
        fields = ['title', 'file', 'description']
        exclude = ['creator', 'size', 'date']
        widgets = {
            
            'title': TextInput(attrs={
                'class': 'create__input-wrapper',
            }),
            'description': TextInput(attrs={
                'class': 'create__input-wrapper',
            }),
            'file': FileInput(attrs={
                'class': 'create__input-wrapper'
            })
        }

class EditProjectForm(ModelForm):
    class Meta:
        model = user_project
        exclude = []
        

class ReturnToManagerForm(ModelForm):
    class Meta:
        model = user_project
        fields = ['file']

class CopyProject(forms.Form):
    class Meta:
        model = user_project
        title = forms.CharField(required=False)