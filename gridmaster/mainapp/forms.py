from django.forms import ModelForm, TextInput, DateInput, NumberInput 
from django import forms
from .models import *
import datetime

class CreateProjectForm(ModelForm):
    class Meta:
        model = user_project
        fields = ['title', 'description']
        exclude = []
        widgets = {
            'title': TextInput(attrs={
                'class': 'create__input-wrapper',
            }),
            'description': TextInput(attrs={
                'class': 'create__input-wrapper',
            }),
        }

        
