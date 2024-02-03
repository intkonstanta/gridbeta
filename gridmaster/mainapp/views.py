from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.views.generic import DetailView
from django.template import Library
from json import loads
from .models import *
import random
import logging
logging.basicConfig(level=logging.DEBUG, filename="django_log.log",filemode="w")

@login_required(login_url='login')
def code_editor(request):
    return render(request, 'mainapp/code_editor.html')

@login_required(login_url='login')
def project_manager(request):
    user = request.user
    projects = user_project.objects.filter(creator=user)
    max_size = 5 * 1024
    cloud_percent = round(100 * (sum([int(project.size) for project in projects]) / (max_size)), 1) 
    cloud_free_place = max_size - sum([int(project.size) for project in projects])
    flag_free_place_valid = cloud_percent >= 100
    tip = random.choice(all_tips.objects.all()) # РАБОТАЕТ ТОЛЬКО КОГДА ЕСТЬ ХОТЯ-БЫ ОДИН СОВЕТ ДНЯ
    context = {
        'projects': projects,
        'cloud_percent': str(cloud_percent).replace(",", ".", 1),
        'cloud_free_place': cloud_free_place,
        'flag_free_place_valid': flag_free_place_valid,
        'tip': tip,
    }
    return render(request, 'mainapp/project_manager.html', context)


def layout(request):
    return render(request, 'mainapp/layout_mainapp.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


def code_preview(request):
    if request.method == "POST":
        print(loads(request.body)['title'])
        print(user_project.objects.get( title=loads(request.body)['title'] ))
        response_text = loads(request.body)['title']
        context = {'title': response_text, 'code_preview': None, 'date': None, 'size': None, 'description': None,}
        return render(request, 'mainapp/code_preview.html', context) 
    context = {'title': 'my project', 'code_preview': None, 'date': None, 'size': None, 'description': None,}
    return render(request, 'mainapp/code_preview.html', context) 