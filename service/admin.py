from django.contrib import admin

from .models import Author, Comment, Post
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
