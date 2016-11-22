from rest_framework import serializers, pagination
from rest_framework.response import Response
from .models import Author, Comment, Post, FriendRequest, VISIBILITY_CHOICES
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github',
                  'email', 'firstName', 'lastName', 'bio')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'comment',
                  'contentType', 'published')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'source', 'origin', 'description', 'contentType', 'content',
                  'author', 'categories', 'published', 'visibility', 'comments', 'author')


class PostPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data, size):

        obj = {
            'query': 'posts',
            'count': self.page.paginator.count,
            'size': size,
            'posts': data
        }

        next_link = self.get_next_link()
        previous_link = self.get_previous_link()
        if (next_link):
            obj['next'] = next_link

        if (previous_link):
            obj['previous'] = previous_link

        return Response(obj)


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
        fields = ('id', 'username', 'email', 'last_login',
                  'author', 'date_joined', 'is_active')
