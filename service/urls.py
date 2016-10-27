from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts/$', views.posts_handler_generic),
    url(r'^posts/(?P<id>\d+)/$', views.posts_handler_specific),
    url(r'^author/$', views.author_handler),
    url(r'^friends/$', views.friend_handler),
]
