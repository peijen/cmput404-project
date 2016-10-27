# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20161027_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='author',
            name='firstName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='author',
            name='lastName',
            field=models.CharField(default='', max_length=30),
        ),
    ]
