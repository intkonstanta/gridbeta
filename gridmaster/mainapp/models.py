from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime
import random
import string


class user_project(models.Model):

    def __repr__(self):
        return f"{self.title}"
    

    def __str__(self):
        return self.title

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=23)
    size = models.IntegerField(default = 0)
    date = models.DateField(default = timezone.now)
    description = models.TextField(max_length=200, default = '')
    file = models.FileField(upload_to='codes/', default='codes/default.txt') 
    
    def get_absolute_url(self):
        return f"/mainapp/code_editor/{self.title}"

   
    class Meta:
        verbose_name = "Пользовательский проект"
        verbose_name_plural = "Пользовательские проекты"

        
class all_tips(models.Model):
    title = models.CharField(max_length=23)
    text = models.CharField(max_length=100)
    img = models.ImageField(upload_to='tip_imgs/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Совет дня"
        verbose_name_plural = "Советы дня"

