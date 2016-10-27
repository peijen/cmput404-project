from __future__ import unicode_literals

from django.db import models

import uuid
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=500)
    displayName = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    github = models.CharField(max_length=500)
    userID = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    source = models.CharField(max_length=150)
    origin = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    contentType = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    catagories = models.TextField(null=True)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=100)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=150)
    published = models.DateTimeField(auto_now=True)
