from django.shortcuts import render
from django.http import HttpResponse

def registration(request):
    return render(request, 'usersapp/registration.html')


def login(request):
    return render(request, 'usersapp/login.html')

def reset_code(request):
    return render(request, 'usersapp/reset_code.html')


def reset_pass(request):
    return render(request, 'usersapp/reset_pass.html')


def reset_mail(request):
    return render(request, 'usersapp/reset_mail.html')