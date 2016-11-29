from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core import serializers
from django.utils.safestring import mark_safe
from rest_framework.pagination import PageNumberPagination
from django.contrib.sites.models import Site

from .models import Author, Comment, Post, FriendRequest, Nodes
from .serializers import PostSerializer, AuthorSerializer, UserSerializer, PostPagination, CommentSerializer, FriendRequestSerializer
from .authenticate import check_authenticate

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

import json
import requests
from requests.auth import HTTPBasicAuth
import datetime
import uuid
from operator import itemgetter
import dateutil.parser

# Create your views here.

def index(request):

    # Testing authentication check via HTTP Basic Auth
    authenticated = check_authenticate(request)
    if(authenticated == None):
        return HttpResponse("Not authenticated")
    else:
        return HttpResponse("Authenticated as user" + authenticated.username)

def catch_em_all(request):

    nodes = Nodes.objects.all()

    posts = []

    for node in nodes:

        if node.useauth:
            stuff = requests.get(node.url + "posts/", auth=HTTPBasicAuth(node.username, node.password))
            print stuff.content
        else:
            stuff = requests.get(node.url + "posts/")
            print stuff.content

        content = json.loads(stuff.content)

        if str(stuff.status_code)[:1] != "2":
            continue

        for post in content['posts']:
            posts.append(post)

    return posts


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
    new_post.source = "http://cmput404t02.herokuapp.com/service/posts/%s" % (new_post.id)
    new_post.origin = "http://cmput404t02.herokuapp.com/service/posts/%s" % (new_post.id)
    new_post.save()
    return new_post

def create_json_response_with_location(data, id, path):
    json_response = JsonResponse(data)
    json_response['Location'] = path + str(id)
    json_response.status_code = 201
    return json_response

@api_view(['GET', 'POST'])
def posts_comments_handler(request, id):

    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponse(status=404)

    #Do they have access to this?
    if(post.visibility == "PRIVATE"):
        return HttpResponse(status=404)
    elif(post.visibility == "SERVERONLY" and request.META['HTTP_HOST'] != get_host(True)):
        return HttpResponse(status=404)

    #Add friend check here, etc.

    if(request.method == 'POST'):

        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)
        try:
            author = Author.objects.get(user_id=user.id)
        except:
            return HttpResponse(status=403)

        comment = request.data
        new_comment = Comment.objects.create(
                post_id = id,
                author_id = request.user.author.id,
                comment = comment['comment'],
                contentType = comment['contentType']
            )

        serializer = CommentSerializer(new_comment)
        json_data = JSONRenderer().render(serializer.data)

        return HttpResponse(json_data, content_type='application/json')

    elif(request.method == 'GET'):

        #Todo: show all comments for this post
        return HttpResponse('')


@api_view(['GET', 'POST', 'PUT'])
def posts_handler_generic(request):

    if (request.method == 'POST'):
        # TODO: ADD validation
        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)
        try:
            author = Author.objects.get(user_id=user.id)
        except:
            return HttpResponse(status=403)

        post = request.data.copy()
        post['author_id'] = author.id

        created = create_post(post)
        created.comments = []

        serializer = PostSerializer(created)

        json_data = JSONRenderer().render(serializer.data)

        response = HttpResponse(json_data, content_type='application/json')
        response.status = 201
        response['Location'] = request.path + str(created.id)

        return response

    elif (request.method == 'GET'):

        size = int(request.GET.get('size', 25))
        paginator = PostPagination()
        paginator.page_size = size
        posts = Post.objects.filter(visibility = 'PUBLIC').order_by('-published')
        result_posts = paginator.paginate_queryset(posts, request)

        for post in result_posts:
            comments = Comment.objects.filter(post_id=post['id']).order_by('-published')[:5]
            author = Author.objects.get(id=post['author_id'])
            post['comments'] = comments
            post['author'] = author
            post['count'] = comments.count()
            post['size'] = size
            post['next'] = post.origin + '/posts/' + str(post.id) + '/comments'

        serializer = PostSerializer(result_posts, many=True)
        return paginator.get_paginated_response(serializer.data, size)

    elif (request.method == 'PUT'):
        # TODO: VALIDATION... again
        body = json.loads(request.body)
        new_post = create_post(body)
        data = model_to_dict(new_post)
        return create_json_response_with_location(data, new_post.id, request.path)


def posts_handler_specific(request, id):

    if (request.method == 'POST'):
        return HttpResponse(status=405)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        body = json.loads(request.body)
        post = Post.objects.get(pk=id)
        for k, v in body.iteritems():
            post[k] = v
        post.save()
        return HttpResponse(status=200)

    elif (request.method == 'GET'):
        # validation to see if they can actually access this post based on its
        # permissions
        post = Post.objects.get(pk=id)
        post['comments'] = Comment.objects.filter(post_id=post.id)
        post['author'] = Author.objects.get(id=post.author_id)
        serializer = PostSerializer(post)
        json_data = JSONRenderer().render(serializer.data)

        return HttpResponse(json_data, content_type='application/json')

    elif (request.method == 'DELETE'):

        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)

        try:
            post = Post.objects.get(pk=id)
        except:
            return HttpResponse(status=404)

        try:
            author = Author.objects.get(user_id=user.id)
            pass

        except Exception as e:

            return HttpResponse(status=403)
            raise

        if(post.author_id == author.id):
            post.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)


def specific_author_posts_handler(request, id):

    return HttpResponse(catch_em_all(request))

def author_posts_handler_linked(request):
    #Posts that are visible to the currently authenticated user

    if (request.method == 'GET'):

        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)
        try:
            author = Author.objects.get(user_id=user.id)
        except:
            return HttpResponse(status=404)

        host = "http://127.0.0.1:8000/"

        service_link = get_service_link()
        my_friends = user.friends.all()

        #Deal with friends and stuff here later.
        posts = Post.objects.filter(
            Q(author = author.id) | Q(visibility = 'PUBLIC') | Q(author__in = my_friends)
            ).order_by('-published')

        #count = posts.count()

        #posts = posts[::1]

        #Check/get page size
        if 'size' not in request.GET:
            page_size = 25
        else:
            try:
                page_size = int(request.GET['size'])
            except:
                page_size = 25

        #Check/get current page
        if 'page' not in request.GET:
            current_page = 0
        else:
            try:
                current_page = int(request.GET['page'])
            except:
                current_page = 0

        count = len(posts)

        returnjson = {}
        returnjson['query'] = "posts"
        returnjson['count'] = count
        returnjson['size'] = page_size

        if (current_page * page_size + page_size) < count:
            returnjson['next'] = service_link + "author/posts?page=" + str((current_page + 1))
        if(current_page != 0):
            returnjson['previous'] = service_link + "author/posts?page=" + str((current_page - 1))

        returnjson['posts'] = []

        other_posts = catch_em_all(request)
        #posts.append(other_posts)
        #posts = sorted(posts.items(), key=itemgetter('published'))

        for item in posts[current_page*page_size:current_page*page_size+page_size]:
            workingdict = {}
            workingdict['title'] = item.title
            workingdict['source'] = item.source
            workingdict['origin'] = item.origin
            workingdict['description'] = item.description
            workingdict['contentType'] = item.contentType
            workingdict['content'] = mark_safe(item.content)
            workingdict['id'] = item.id
            workingdict['published'] = item.published.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            workingdict['categories'] = item.categories.split(",")
            comments = item.comment_set.all().order_by('-published')
            workingdict['author'] = {}
            workingdict['author']['id'] = item.author.id
            workingdict['author']['host'] = item.author.host
            workingdict['author']['displayName'] = item.author.displayName
            workingdict['author']['url'] = item.author.url
            workingdict['author']['github'] = item.author.github


            workingdict['visibility'] = item.visibility
            workingdict['count'] = comments.count()
            workingdict['size'] = page_size
            workingdict['next'] = service_link + "posts/" + str(item.id) + "/comments"
            workingdict['comments'] = []
            for comment in comments[:5]:
                workingcomment = {}
                workingcomment['author'] = {}
                workingcomment['author']['id'] = comment.author.id
                workingcomment['author']['host'] = comment.author.host
                workingcomment['author']['displayName'] = comment.author.displayName
                workingcomment['author']['url'] = comment.author.url
                workingcomment['author']['github'] = comment.author.github
                workingcomment['comment'] = comment.comment
                workingcomment['contentType'] = comment.contentType
                workingcomment['published'] = comment.published.strftime("%Y-%m-%dT%H:%M:%S+00:00")
                workingcomment['id'] = comment.id
                workingdict['comments'].append(workingcomment)


            returnjson['posts'].append(workingdict)

        for item in other_posts:
            returnjson['posts'].append(item)

        #posts = sorted(posts.items(), key=itemgetter('published'))

        returnjson['posts'] = sorted(returnjson['posts'], key=itemgetter('published'))

        returnjson['count'] = len(returnjson['posts'])

        return JsonResponse(returnjson)

    return HttpResponse(status=405)

@api_view(['GET'])
def author_posts_handler(request):
    #Posts that are visible to the currently authenticated user

    if (request.method == 'GET'):

        user = check_authenticate(request)
        if(user == None):
            return HttpResponse(status=403)
        try:
            author = Author.objects.get(user_id=user.id)
        except:
            return HttpResponse(status=404)

        my_friends = author.friends.all()

        print my_friends

        #Deal with friends and stuff here later.
        posts = Post.objects.filter(
            Q(author = author.id) | Q(visibility = 'PUBLIC') | Q(author__in = my_friends)
            ).order_by('-published')

        size = int(request.GET.get('size', 25))
        paginator = PostPagination()
        paginator.page_size = size
        result_posts = paginator.paginate_queryset(posts, request)

        for post in result_posts:
            comments = Comment.objects.filter(post_id=post['id']).order_by('-published')[:5]
            author = Author.objects.get(id=post['author_id'])
            post['comments'] = comments
            post['author'] = author
            post['count'] = comments.count()
            post['size'] = size
            post['next'] = post.origin + '/posts/' + str(post.id) + '/comments'

        serializer = PostSerializer(result_posts, many=True)
        return paginator.get_paginated_response(serializer.data, size)

    return HttpResponse(status=405)

def get_host(removeTrailingSlash=False):
    host = Site.objects.get_current().domain

    if removeTrailingSlash:
        if host.endswith('/'):
            host = host[:-1]

    return host

def get_service_link():
    service_link = get_host() + "service/"
    return service_link

def author_handler(request, id):
    #Return the foreign author's profile
    if (request.method == 'POST'):
        return HttpResponse("")

    elif (request.method == 'GET'):

        author = Author.objects.get(id=id)
        author.friends = author.friends.all()
        author.url = author.host + 'author/' + str(author.id)
        serializer = AuthorSerializer(author)
        json_data = JSONRenderer().render(serializer.data)

        return HttpResponse(json_data, content_type='application/json')

def friend_handler(request):
    if (request.method == 'GET'):
        author = Author.objects.get(user_id=request.user.id)
        friends = author.friends.all()
        serializer = AuthorSerializer(friends, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    return HttpResponse(status=405)

def friend_handler_specific(request, id):
    if (request.method == 'DELETE'):
        author = Author.objects.get(user_id=request.user.id)

        try:
            friend = Author.objects.get(id=id)
            author.friends.remove(friend)
            return HttpResponse(status=200)

        except:
            return HttpResponse(status=404)

    elif (request.method == 'GET'):

        try :
            author = Author.objects.get(user_id=request.user.id)
            friend = author.friends.filter(id=id)[0]

            authors = [author.id]
            if (friend):
                authors.append(friend.id)
            obj = {
                'query': 'friends',
                'authors': authors,
            }

            json_data = json.dumps(obj)
            return HttpResponse(json_data, content_type='application/json')

        except:
            return HttpResponse(status=404)

    elif (request.method == 'POST'):
        try:
            author = Author.objects.get(id=id)
            json_body = json.loads(request.body)
            friends = map(lambda x:x.id, author.friends.filter(pk__in=json_body['authors']))

            obj = {
                'query': 'friends',
                'author': str(id),
                'authors': friends,
            }

            json_data = json.dumps(obj)
            return HttpResponse(json_data, content_type='application/json')

        except:
            return HttpResponse(status=404)

    return HttpResponse("")

def friend_query_handler(request, author1_id, author2_id):
    if (request.method == 'GET'):
        try:
            author1 = Author.objects.get(id=author1_id)
            author2 = Author.objects.get(id=author2_id)

            friends1 = author1.friends.filter(id=author2_id)
            friends2 = author2.friends.filter(id=author1_id)

            authors = [author1.id, author2.id]

            obj = {
                'query': 'friends',
                'authors': authors,
            }

            obj['friends'] = len(friends1) > 0 and len(friends2) > 0
            json_data = json.dumps(obj)

            return HttpResponse(json_data, content_type='application/json')


        except:
            # authors not found
            return HttpResponse(status=404)

# {
# 	"query":"friendrequest",
# 	"author": {
# 	    # UUID
# 		"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
# 		"host":"http://127.0.0.1:5454/",
# 		"displayName":"Greg Johnson"
# 	},
# 	"friend": {
# 	    # UUID
# 		"id":"de305d54-75b4-431b-adb2-eb6b9e637281",
# 		"host":"http://127.0.0.1:5454/",
# 		"displayName":"Lara Croft",
# 		"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
# 	}
# }

# return friend request if exists, otherwise false
def friend_request_exists(author_id, friend_id):
    try:
        fr = FriendRequest.objects.get(requester_id=author_id, requestee_id=friend_id)
        return fr

    except:
        return False

def friendrequest_handler(request):

    if (request.method == 'POST'):
        # TODO: validation, are they already friends?
        body = json.loads(request.body)

        try:
            me = Author.objects.get(user_id=request.user.id)

        except:
            if (me.id != requester_id):
                return HttpResponse(status=401)

        try:
            me.friends.get(id=body['friend']['id'])
            return HttpResponse(status=409)
        except:
            pass

        fr = friend_request_exists(body['author']["id"], body['friend']['id'])

        if (fr):
            return HttpResponse(status=409)

        # try to get an existing reverse friend request (where the requester is the requestee)
        try:
            bidirectional = FriendRequest.objects.get(requestee_id=body['author']['id'], requester_id=body['friend']['id'])

            # exists a friend request from the other user, even if it was previously rejected
            # make users friends

            friend1 = Author.objects.get(id=bidirectional.requester.id)
            friend2 = Author.objects.get(id=bidirectional.requestee.id)


            if friend1.id != friend2.id:
                friend1.friends.add(friend2)
                friend2.friends.add(friend1)

            bidirectional.delete()

            return HttpResponse(status=201)


        except:
            fr = FriendRequest.objects.create(requester_id=body['author']['id'], requestee_id=body['friend']['id'])
            data = model_to_dict(fr)
            return create_json_response_with_location(data, fr.id, request.path)

    # return users list of pending requests
    elif (request.method == 'GET'):

        author = Author.objects.get(user_id=request.user.id)
        friend_requests = FriendRequest.objects.filter((Q(requestee_id=author.id) & Q(accepted__isnull=True)))
        for friend_request in friend_requests:
            setattr(friend_request, 'author', Author.objects.get(id=friend_request.requester_id))
            setattr(friend_request, 'friend', Author.objects.get(id=friend_request.requestee_id))

        serializer = FriendRequestSerializer(friend_requests, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    else:
        return HttpResponse(status=405)


def get_me(request):

    if not request.user:
        return HttpResponse(status=401)

    serializer = UserSerializer(request.user)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')
