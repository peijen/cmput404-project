from __future__ import unicode_literals

from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    authorID = models.ForeignKey(Authors, on_delete=models.CASCADE)


class Author():
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField()
    displayName = models.CharField(max_length=50)
    url = models.CharField()
    github = models.CharField()
