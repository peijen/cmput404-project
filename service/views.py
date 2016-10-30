from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Author, Comment, Post
from django.forms.models import model_to_dict
from django.core import serializers
from .authenticate import check_authenticate

# Create your views here.
def index(request):
    
    #Testing authentication check via HTTP Basic Auth
    authenticated = check_authenticate(request)

    if(authenticated == None):
        return HttpResponse("Not authenticated")
    else:
        return HttpResponse("Authenticated as user" + authenticated.username)

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

def posts_handler_specific(request, id):
	if (request.method == 'POST'):
		return HttpResponse(status=405)
	elif (request.method == 'PUT' or request.method == 'PATCH'):
		return
		#update an entry
	elif (request.method == 'GET'):
		#validation to see if they can actually access this post based on its permissions
		post = Post.objects.get(pk=id)
		serialized_post = serializers.serialize('json', [post])
		return JsonResponse(serialized_post, safe=False)
	elif (request.method == 'DELETE'):
		#validation to see if they can actually delete the object, i.e it's their post
		post = Post.objects.get(pk=id)
		post.delete()
		return HttpResponse(status=200)

def author_handler(request):
	if (request.method == 'POST'):
		return
	return HttpResponse("")

def friend_handler(request):
	return HttpResponse("My united states of")
