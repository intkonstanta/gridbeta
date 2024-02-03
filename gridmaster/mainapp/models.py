from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class user_project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=23)
    size = models.IntegerField()
    date = models.DateField()
    description = models.TextField(max_length=200)
    file = models.TextField(max_length=160000)

    def code_preview_convert(count, code_text):
        '''
        arg: x - int, code - string
        count: first x '\n' symbols and return part of code
        return: code_preview - string
        '''
        return 'codepreviewbeta'

    code_preview = code_preview_convert(20, file)

    TEMPLATE_PREVIEW = 'mainapp/code_preview.html'
    # def get_absolute_url(self):
    #     return reverse('preview', kwargs={'title':f'{self.title}', 'code':f'{self.description}',})

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Пользовательский проект"
        verbose_name_plural = "Пользовательские проекты"

        
class all_tips(models.Model):
    title = models.CharField(max_length=23)
    text = models.CharField(max_length=80)
    img = models.ImageField(upload_to='tip_imgs/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Совет дня"
        verbose_name_plural = "Советы дня"

