#!python
# log/urls.py
from django.conf.urls import url
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
#from .views import register

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^register/$', views.UserRegisterForm.as_view(), name='register'),
    url(r'^login/register/$', views.UserRegisterForm.as_view(), name='register'),
    url(r'^make_post/$', views.make_post, name ='make_post'),
    url(r'^profile/$', views.update_profile, name='update_profile'),
    url(r'^author/(?P<id>[^/]+)/?$', views.view_profile, name='view_profile'),
]
