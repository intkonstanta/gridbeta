# Generated by Django 5.0.1 on 2024-01-31 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=23)),
                ('size', models.IntegerField()),
                ('date', models.DateField()),
                ('description', models.TextField(max_length=200)),
                ('file', models.TextField(max_length=160000)),
            ],
        ),
    ]