from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, Comment, Post
from django.core import serializers
import json

# Create your views here.
def index(request):
	return HttpResponse("At the service index")

def posts_handler(request):
	if (request.method == 'POST'):
		#TODO: ADD validation
		post = request.POST
		new_post = Post.objects.create(title=post['title'], author_id=post['author_id'])
	return HttpResponse("Whatever")

def author_handler(request):
	if (request.method == 'POST'):
	return HttpResponse("")

def friend_handler(request):
	return HttpResponse("My united states of")
