from django.shortcuts import render
from django.http import HttpResponse

def code_editor(request):
    return render(request, 'mainapp/code_editor.html')


def project_manager(request):
    return render(request, 'mainapp/project_manager.html')


def layout(request):
    return render(request, 'mainapp/layout_mainapp.html')
