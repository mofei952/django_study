#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/3 22:16
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^jigsaw', views.jigsaw),
    url(r'^llk$', views.llk),
    url(r'^llk/icon_map', views.llk_icon_map),
    url(r'^llk/connected', views.llk_connected),
    url(r'^llk/status', views.llk_status),
    url(r'^llk/hint', views.llk_hint)
]
