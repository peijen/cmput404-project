# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 21:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=500)),
                ('displayName', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=500)),
                ('github', models.CharField(max_length=500)),
                ('email', models.EmailField(default='', max_length=254)),
                ('firstName', models.CharField(default='', max_length=30)),
                ('lastName', models.CharField(default='', max_length=30)),
                ('bio', models.TextField(default='')),
                ('friends', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
                ('userID', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=150)),
                ('published', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('source', models.CharField(max_length=150)),
                ('origin', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('contentType', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('categories', models.TextField(null=True)),
                ('published', models.DateTimeField(auto_now=True)),
                ('visibility', models.CharField(choices=[('0', 'ME'), ('1', 'OTHER_AUTHOR'), ('2', 'FRIENDS'), ('3', 'FRIENDS_OF_FRIENDS'), ('4', 'HOST_FRIENDS'), ('5', 'ALL')], default='0', max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Post'),
        ),
    ]
