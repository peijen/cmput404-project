from rest_framework import serializers
from .models import Author, Comment, Post, FriendRequest, VISIBILITY_CHOICES
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github', 'email', 'firstName', 'lastName', 'bio')

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'comment', 'contentType', 'published')

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'published', 'visibility', 'comments', 'author')

class FriendRequestSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    friend = AuthorSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id', 'author', 'friend', 'accepted', 'created')

class UserSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_login', 'author', 'date_joined', 'is_active')
