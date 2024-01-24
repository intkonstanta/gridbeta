from django.urls import path
from . import views

urlpatterns = [
    path('code_editor/', views.code_editor),
    path('project_manager/', views.project_manager),
    path('layout/', views.layout),
    
] 