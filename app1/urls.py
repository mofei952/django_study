#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/3 16:05
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from django.urls import path, re_path

from app1 import views

urlpatterns = [
    url(r'^articlelist/', views.articlelist),
    url(r'^addarticle/', views.addarticle),
    path(r'hello/', views.hello),
    url(r'^hello/(\d+)', views.hello2),
    url(r'^test/(?P<id>\d{2})/', views.test),
    # re_path(r'^blog/(page-(\d+)/)?$', views.test2),                  # bad
    # re_path(r'^comments/(?:page-(?P<page_number>\d+)/)?$', views.test3),  # good
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
    # re_path('blog/(?:page-(\d+)/)?',views.page)
]


