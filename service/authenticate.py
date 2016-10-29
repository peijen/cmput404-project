from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def check_authenticate(request):

	# Attempts to authenticate via HTTP Basic Auth. Returns None if the
	# authentication failed (either no header or wrong login), or it returns
	# the user the authentication succeeded on.


	header = request.META.get('HTTP_AUTHORIZATION')
	
	
	if header == None:
		return None
	
	
	# Split this header into two. First word should be basic because we only
	# support basic auth.

	parsed = header.split(" ")
	if(parsed[0] != "Basic"):
		return None

	# Get the argument after the space. Should be login info encoded into
	# base 64. If this fails header is invalid, return None.
	try:
		logindata = parsed[1].decode('base 64')
	except:
		return None

	# Username and password is separated by a :, split it.

	# TODO: Username/Passwords that have : are supposed to be percent encoded.
	# fix this later??? Just assume no : for now.

	logindata = logindata.split(":", 1)


	# Authenticate with Django. Returns the user if correct, otherwise
	# returns None.
	try:
		user = authenticate(username=logindata[0], password=logindata[1])
	except:
		return None
	
	if(user == None):
		return None
	else:
		return user





