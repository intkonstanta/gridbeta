from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class user_project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=23)
    size = models.IntegerField()
    date = models.DateField()
    description = models.TextField(max_length=200)
    file = models.TextField(max_length=160000)

    def __str__(self):
        return self.title

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

