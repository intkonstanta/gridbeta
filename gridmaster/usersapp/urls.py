from django.urls import path
from . import views
from django.urls import path, reverse_lazy


from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)



urlpatterns = [
    path('registration/', views.registration_user, name = 'registration'),
    path('login/', views.login_user, name='login'), 
    path('reset_pass/', views.reset_pass, name = 'reset_pass'),
    path('reset_mail/', views.reset_mail, name = 'reset_mail'),
    path('reset_code/', views.reset_code, name = 'reset_code'),

    path('password_reset/', PasswordResetView.as_view(template_name='usersapp/reset_mail.html',
                                                  email_template_name='usersapp/password_reset_email.html',
                                                  success_url=reverse_lazy("password_reset_done")), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='usersapp/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='usersapp/password_reset_confirm.html',
                                                                             success_url=reverse_lazy("password_reset_complete")), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='usersapp/password_reset_complete.html'), name='password_reset_complete'),
] 
