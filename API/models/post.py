from django.db import models

VISIBILITY_CHOICES = (
    ('0', 'ME'),
    ('1', 'OTHER_AUTHOR'),
    ('2', 'FRIENDS'),
    ('3', 'FRIENDS_OF_FRIENDS'),
    ('4', 'HOST_FRIENDS'),
    ('5', 'ALL')
)

class Post(models.Model):
    body = models.TextField()
    visiblity = models.CharField(max_length=1, choices=VISIBILITY_CHOICES, default='0')
