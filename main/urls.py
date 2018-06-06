from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path
from main.views import *
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.display, name='display'),
    url(r'^manage', views.manage, name='manage'),
    url(r'^add', views.add, name='add'),
    url(r'^detay', views.detail, name='detail')
]