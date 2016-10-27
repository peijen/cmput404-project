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
