from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Author, Comment, Post, FriendRequest
from .serializers import PostSerializer, AuthorSerializer
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core import serializers
from .authenticate import check_authenticate
from django.contrib.sites.models import Site
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

def posts_comments_handler(request, id):

    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponse(status=404)

    current_host = get_host

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

        comment = json.loads(request.body)

        comment['post'] = post.id
        comment['author'] = author.id

        #comment['comment'] = "test"
        #comment['contentType'] = "text/plain"

        new_comment = Comment.objects.create(
                post_id = comment['post'],
                author_id = comment['author'],
                comment = comment['comment'],
                contentType = comment['contentType']
            )

        comment['id'] = new_comment.id
        comment['published'] = new_comment.published.strftime("%Y-%m-%dT%H:%M:%S+00:00")

        return HttpResponse(json.dumps(comment))

    elif(request.method == 'GET'):

        #Todo: show all comments for this post
        return HttpResponse('')



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

        post = json.loads(request.body)

        #post = {}
        #post["title"] = "hello"
        #post["description"] = "desc"
        #post["content"] = "test"
        #post["categories"] = "cat"
        #post["visibility"] = "ALL"

        post['source'] = "http://127.0.0.1:8000/posts/fixthislater"
        post['origin'] = "http://127.0.0.1:8000/posts/originfixthislater"
        post['author_id'] = author.id

        created = create_post(post)

        post['id'] = created.id

        dict_obj = model_to_dict(created)

        serialized = json.dumps(dict_obj)
        return HttpResponse(serialized, content_type="/application/json")

        #return create_json_response_with_location(data, new_post.id, request.path)

    elif (request.method == 'GET'):
        # TODO: this should return all the posts that a user can see, i.e their
        # stream, not all posts in db
        posts = Post.objects.all()
        for post in posts:
            comments = Comment.objects.filter(post_id=post['id'])
            author = Author.objects.get(id=post['author_id'])
            post['comments'] = comments
            post['author'] = author

        serializer = PostSerializer(posts, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

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
        dict_obj = model_to_dict(post)
        serialized = json.dumps(dict_obj)
        return HttpResponse(serialized, content_type="/application/json")

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

        host = "http://127.0.0.1:8000/"

        service_link = get_service_link()

        #Deal with friends and stuff here later.
        posts = Post.objects.filter(
            Q(author = author.id) | Q(visibility = 'PUBLIC')
            ).order_by('-published')

        count = posts.count()

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

        returnjson = {}
        returnjson['query'] = "posts"
        returnjson['count'] = posts.count()
        returnjson['size'] = page_size

        if (current_page * page_size + page_size) < count:
            returnjson['next'] = service_link + "author/posts?page=" + str((current_page + 1))
        if(current_page != 0):
            returnjson['previous'] = service_link + "author/posts?page=" + str((current_page - 1))

        returnjson['posts'] = []

        for item in posts[current_page*page_size:current_page*page_size+page_size]:
            workingdict = {}
            workingdict['title'] = item.title
            workingdict['source'] = item.source
            workingdict['origin'] = item.origin
            workingdict['description'] = item.description
            workingdict['contentType'] = item.contentType
            workingdict['content'] = item.content
            workingdict['id'] = item.id
            workingdict['published'] = item.published.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            workingdict['categories'] = item.categories.split(",")
            comments = item.comment_set.all().order_by('-published')
            workingdict['author'] = {}
            workingdict['author']['id'] = item.author.id
            workingdict['author']['host'] = item.author.host
            workingdict['author']['displayname'] = item.author.displayName
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

        return JsonResponse(returnjson)


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

        response = {}
        response['id'] = author.id
        response['host'] = get_host()
        response['displayName'] = author.displayName
        response['url'] = get_host() + "author/" + str(author.id)

        #Add friends here later
        response['friends'] = []

        response['github_username'] = author.github
        response['first_name'] = author.firstName
        response['last_name'] = author.lastName
        response['email'] = author.email
        response['bio'] = author.bio

        return JsonResponse(response)


def friend_handler(request):
    if (request.method == 'GET'):
        author = Author.objects.get(user_id=request.user.id)
        friends = author.friends.all()
        serializer = AuthorSerializer(friends, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    return HttpResponse("My united states of")

def friend_handler_specific(request, id):
    if (request.method == 'DELETE'):
        author = Author.objects.get(user_id=request.user.id)

        try:
            friend = Author.objects.get(id=id)
            author.friends.remove(friend)
            return HttpResponse(status=200)

        except:
            return HttpResponse(status=404)

    if (request.method == 'GET'):
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

    return HttpResponse("")
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
def friend_request_exists(requester_id, requestee_id):
    try:
        fr = FriendRequests.objects.get(requester_id=requester_id, requestee_id=requestee_id)
        return fr

    except:
        return False

def friendrequest_handler(request):
    if (request.method == 'POST'):
        # TODO: validation, are they already friends?
        body = json.loads(request.body)

        # try to get an existing reverse friend request (where the requester is the requestee)
        try:
            bidirectional = FriendRequest.objects.get(requestee_id=body['author']['id'], requester_id=body['friend']['id'])

            # exists a friend request from the other user, even if it was previously rejected
            # make users friends

            friend1 = Author.objects.get(id=bidirectional.requester.id)
            friend2 = Author.objects.get(id=bidirectional.requestee.id)

            friend1.friends.add(friend2)
            friend2.friends.add(friend1)
            bidirectional.delete()

            return HttpResponse(status=201)


        except:
            # only create the friend request if it doesn't already exist and wasn't rejected
            fr = friend_request_exists(body['author']['id'], body['friend']['id'])

            if not fr:
                fr = FriendRequest.objects.create(requester_id=body['author']['id'], requestee_id=body['friend']['id'])
                data = model_to_dict(fr)
                return create_json_response_with_location(data, fr.id, request.path)

            else:
                # friend request exists, either pending or rejected
                return HttpResponse(status=409)

    # return users list of pending requests
    elif (request.method == 'GET'):
        author = Author.objects.get(user_id=request.user.id)
        friend_requests = FriendRequest.objects.filter((
            Q(requester_id=author.id) | Q(requestee_id=author.id)) & Q(accepted__isnull=True))
        serialized = serializers.serialize('json', friend_requests)
        return HttpResponse(serialized, content_type="application/json")

    else:
        return HttpResponse(status=405)
