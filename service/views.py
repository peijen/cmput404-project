from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Author, Comment, Post, FriendRequest
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core import serializers
from .authenticate import check_authenticate
import json

# Create your views here.

def index(request):

    # Testing authentication check via HTTP Basic Auth
    authenticated = check_authenticate(request)
    if(authenticated == None):
        return HttpResponse("Not authenticated")
    else:
        return HttpResponse("Authenticated as user" + authenticated.username)


def create_post(post):
    new_post = Post.objects.create(title=post['title'],
                                   source=post['source'],
                                   origin=post['origin'],
                                   author_id=post['author_id'],
                                   description=post['description'],
                                   contentType=post['contentType'],
                                   content=post['content'],
                                   categories=post['categories'],
                                   visibility=post['visibility'])
    return new_post

def create_json_response_with_location(data, id, path):
    json_response = JsonResponse(data)
    json_response['Location'] = path + str(id)
    json_response.status_code = 201
    return json_response


def posts_handler_generic(request):

    if (request.method == 'POST'):
        # TODO: ADD validation
        post = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
        new_post = create_post(post)
        data = model_to_dict(new_post)
        return create_json_response_with_location(data, new_post.id, request.path)

    elif (request.method == 'GET'):
        # TODO: this should return all the posts that a user can see, i.e their
        # stream, not all posts in db
        posts = Post.objects.all()
        serialized_posts = serializers.serialize('json', posts)
        return JsonResponse(serialized_posts, safe=False)

    elif (request.method == 'PUT'):
        # TODO: VALIDATION... again
        body = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
        new_post = create_post(body)
        data = model_to_dict(new_post)
        return create_json_response_with_location(data, new_post.id, request.path)


def posts_handler_specific(request, id):

    if (request.method == 'POST'):
        return HttpResponse(status=405)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        body = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
        post = Post.objects.get(pk=id)
        for k, v in body.iteritems():
            post[k] = v
        post.save()
        return HttpResponse(status=200)

    elif (request.method == 'DELETE'):
        # validation to see if they can actually access this post based on its
        # permissions
        post = Post.objects.get(pk=id)
        serialized_post = serializers.serialize('json', [post])
        return JsonResponse(serialized_post, safe=False)

    elif (request.method == 'GET'):

        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)

        try:
        	author = Author.objects.get(user_id=user.id)
        	post = Post.objects.get(pk=id)
        except:
        	return HttpResponse(status=404)

        if(post.author_id == author.id):
            post.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)


def author_handler(request):
    if (request.method == 'POST'):
        return
    return HttpResponse("")


def friend_handler(request):
    return HttpResponse("My united states of")


def friendrequest_handler(request):
    if (request.method == 'POST'):
        body = json.loads(request.body.strip("'<>() ").replace('\'', '\"'))
        author = Author.objects.get(user_id=request.user.id)
        # TODO: validation, are they already friends?
        fr = FriendRequest.objects.create(
            requester_id=author.id, requestee_id=body['author_id'])
        data = model_to_dict(fr)
        return create_json_response_with_location(data, fr.id, request.path)

    # return users list of pending requests
    elif (request.method == 'GET'):
        author = Author.objects.get(user_id=request.user.id)
        friend_requests = FriendRequest.objects.filter((
            Q(requester_id=author.id) | Q(requestee_id=author.id)) & Q(accepted__isnull=True))
        serialized = serializers.serialize('json', friend_requests)
        return JsonResponse(serialized, safe=False)

    else:
        return HttpResponse(status=405)
