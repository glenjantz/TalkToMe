from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^makeroom$', views.makeroom),
    url(r'^chatroom$', views.chatroom),
    url(r'^deleteroom/(?P<roomid>\d+)$', views.deleteroom),
    url(r'^addmessage/(?P<roomid>\d+)$', views.addmessage),
    url(r'^logout$', views.logout),
    url(r'^.+$', views.index),
]
