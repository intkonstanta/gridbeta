from django.urls import path
from . import views


urlpatterns = [
    path('registration', views.registration_user, name = 'registration'),
    path('login', views.login_user, name='login'), 
    path('reset_pass', views.reset_pass, name = 'reset_pass'),
    path('reset_mail', views.reset_mail, name = 'reset_mail'),
    path('reset_code', views.reset_code, name = 'reset_code'),
] 
