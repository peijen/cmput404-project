#!python
# log/urls.py
from django.conf.urls import url
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/register.html/$', CreateView.as_view(
        template_name='register.html', form_class=UserCreationForm,
        success_url='/')),
   
]
