#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/7 18:08
# @File    : extra_filters.py
# @Software: PyCharm

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def cut_filter(value, arg):
    return value(arg, '')


# register.filter(name='cut_filter', filter_func=cut_filter)

@register.filter
@stringfilter
def lower2(value):
    return value.lower()


@register.filter(is_safe=True)
def add(value, arg):
    return mark_safe('%s %s' % (value, arg))


@register.filter
def get_attr(d, attr_name):
    return getattr(d, attr_name)


@register.filter
def get_key(d, key_name):
    return d.get(key_name)
