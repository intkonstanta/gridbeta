from django.urls import path
from . import views
from .models import all_tips


urlpatterns = [
    path('code_editor/<title>/', views.code_editor, name='code_editor'),
    path('project_manager/', views.project_manager, name='project_manager'),
    path('logout/', views.logoutUser, name="logout"),
    path('code_preview/', views.code_preview, name='code_preview'),
    path('get_rendered_code/', views.get_rendered_code, name='rendered_code')
    
] 
