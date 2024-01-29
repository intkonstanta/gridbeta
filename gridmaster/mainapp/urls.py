from django.urls import path
from . import views

urlpatterns = [
    path('code_editor', views.code_editor, name='code_editor'),
    path('project_manager', views.project_manager, name='project_manager'),
    path('logout', views.logoutUser, name="logout")
    
] 