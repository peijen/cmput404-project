from django.contrib import admin

from .models import Author, Comment, Post, FriendRequest
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(FriendRequest)
admin.site.register(Nodes)
