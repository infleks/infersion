from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path
from main.views import *
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.display, name='display'),
    url(r'^manage', views.manage, name='manage'),
    url(r'^add$', views.add, name='add'),
    url(r'^edit', views.edit, name='edit'),
    url(r'^addCus$', views.addCus, name='addCus'),
    url(r'^addTechMan$', views.addTechMan, name='addTechMan'),
    url(r'^addProdVer$', views.addProdVer, name='addProdVer'),
    url(r'^addProdMan$', views.addProdMan, name='addProdMan'),
    url(r'^addDB$', views.addDB, name='addDB'),
    url(r'^addDbVer$', views.addDbVer, name='addDbVer'),
    url(r'^addServer$', views.addServer, name='addServer'),
    url(r'^addServerVer$', views.addServerVer, name='addServerVer'),
    url(r'^addProd$', views.addProd, name='addProd'),
    url(r'^detay', views.detail, name='detail')
]