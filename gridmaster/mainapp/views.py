from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.views.generic import DetailView
from django.template import Library
from django.utils import timezone
from .models import *
from .forms import *
from json import loads
from json import dumps
import logging
import random


logging.basicConfig(level=logging.ERROR, filename="logging_mainapp.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
number_of_displayed_lines = 20
context_preview = None

def code_preview_convert(count, code_text):
        separated_strings = str(code_text).splitlines()
        return '\n'.join(separated_strings[:count])


@login_required(login_url='login')
def code_editor(request):
    return render(request, 'mainapp/code_editor.html')


@login_required(login_url='login')
def project_manager(request):
    user = request.user
    id = user.id
    projects = user_project.objects.filter(creator=user)

    print(user.id)
   
    try:
        tip = random.choice(all_tips.objects.all())
    except Exception:
        tip = None 

    max_size = 5 * 1024
    cloud_percent = round(100 - (100 * (sum([int(project.size) for project in projects]) / (max_size))), 1) 
    cloud_free_place = max_size - sum([int(project.size) for project in projects])
    flag_free_place_valid = cloud_percent < 100
    form = CreateProjectForm(request.POST, auto_id=False, initial = {
            'date': timezone.now,
            'size': 8,
            'file': '#',
            'creator': "intkonst",#request.user.id,
       })
    print(form)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('code_editor')
        else:
            print(form.errors)
    
    context = {
        'cloud_percent': str(cloud_percent).replace(",", ".", 1),
        'cloud_free_place': cloud_free_place,
        'flag_free_place_valid': flag_free_place_valid,
        'tip': tip,
        'form': form,
        }
    

    if len(list(projects)) == 0:
        context['projects'] = None
    else:
        context['projects'] = projects
    
    return render(request, 'mainapp/project_manager.html', context)


def layout(request):
    return render(request, 'mainapp/layout_mainapp.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')
    

def code_preview(request):
    global context_preview
    if request.method == "POST": 
        response_text_title = loads(request.body)['title']
        code_preview_content_object = user_project.objects.get( title=response_text_title )
        converted_code_for_preview = code_preview_convert(number_of_displayed_lines, code_preview_content_object.file)
        
        context_preview = { 'code_preview': converted_code_for_preview,\
                    'title': code_preview_content_object.title,\
                    'date': str(code_preview_content_object.date).replace("-", "."),\
                    'size': code_preview_content_object.size,\
                    'description': code_preview_content_object.description,  
                            }

    if request.method == "GET":
        return JsonResponse(context_preview)

    return HttpResponse("")