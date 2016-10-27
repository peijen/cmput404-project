from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Author, Comment, Post
from django.forms.models import model_to_dict
from django.core import serializers

# Create your views here.
def index(request):
	return HttpResponse("At the service index")

def posts_handler_generic(request):
	if (request.method == 'POST'):
		#TODO: ADD validation
		post = request.POST
		new_post = Post.objects.create(title=post['title'], author_id=post['author_id'])
		response = model_to_dict(new_post)
		return JsonResponse(response)

	elif (request.method == 'GET'):
		#TODO: this should return all the posts that a user can see, i.e their stream, not all posts in db
		posts = Post.objects.all()
		serialized_posts = serializers.serialize('json', posts)
		return JsonResponse(serialized_posts, safe=False)

def posts_handler_specific(request):
	return HttpResponse("")

def author_handler(request):
	if (request.method == 'POST'):
		return
	return HttpResponse("")

def friend_handler(request):
	return HttpResponse("My united states of")
