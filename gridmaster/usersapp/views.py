from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from .models import *
from .forms import CreateUserForm


def registration_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('login')

    context = {'form': form}
    return render(request, 'usersapp/registration.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('project_manager')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_info = authenticate(request, username=username, password=password)
            if user_info is not None:
                login(request, user_info)
                return redirect('project_manager')
            else:
                return redirect('login')

        context = {}
        return render(request, 'usersapp/login.html', context)


def reset_code(request):
    return render(request, 'usersapp/reset_code.html')


def reset_pass(request):
    return render(request, 'usersapp/reset_pass.html')


def reset_mail(request):
    return render(request, 'usersapp/reset_mail.html')