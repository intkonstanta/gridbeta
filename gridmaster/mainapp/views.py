from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from .models import *

@login_required(login_url='login')
def code_editor(request):
    return render(request, 'mainapp/code_editor.html')

@login_required(login_url='login')
def project_manager(request):
    return render(request, 'mainapp/project_manager.html')


def layout(request):
    return render(request, 'mainapp/layout_mainapp.html')

def logoutUser(request):
    logout(request)
    return redirect('login')