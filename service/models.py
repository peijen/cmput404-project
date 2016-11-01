from __future__ import unicode_literals

from django.db import models

import uuid
from django.contrib.auth.models import User

'''
Dealing with no UUID serialization support in json

https://arthurpemberton.com/2015/04/fixing-uuid-is-not-json-serializable
'''
from json import JSONEncoder
from uuid import UUID
JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

VISIBILITY_CHOICES = (
    ('PRIVATE', 'PRIVATE'),
    ('SERVERONLY', 'SERVERONLY'),
    ('FRIENDS', 'FRIENDS'),
    ('FOAF', 'FOAF'),
    ('PUBLIC', 'PUBLIC')
)

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.CharField(max_length=500)
    displayName = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    github = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=254, default="")
    firstName = models.CharField(max_length=30, default="")
    lastName = models.CharField(max_length=30, default="")
    bio = models.TextField(default="")
    friends = models.ForeignKey("self", null=True, blank=True)
    def __str__(self):
        return self.displayName

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    source = models.CharField(max_length=150)
    origin = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    contentType = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.TextField(null=True)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='0')
    def __str__(self):
        return self.title

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, data):
        return setattr(self, key, data)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=150)
    published = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment

class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    requester = models.ForeignKey(Author, related_name="requester") #iniated the friend request
    requestee = models.ForeignKey(Author, related_name="requestee") #received the friend request
    accepted = models.NullBooleanField(null=True) #was the friend request accepted or rejected? if null means request is pending
    created = models.DateTimeField(auto_now=True) #when was the request created
