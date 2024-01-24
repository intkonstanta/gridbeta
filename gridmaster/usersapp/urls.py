from django.urls import path
from . import views


urlpatterns = [
    path('registration', views.registration),
    path('login', views.login), 
    path('reset_pass', views.reset_pass),
    path('reset_mail', views.reset_mail),
    path('reset_code', views.reset_code),
    
] 
