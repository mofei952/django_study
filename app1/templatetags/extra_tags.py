#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/7 16:21
# @File    : extra_tags.py
# @Software: PyCharm
from datetime import datetime
from django import template
from django.template import TemplateSyntaxError

register = template.Library()


class DateNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string

    def render(self, context):
        return datetime.now().strftime(self.format_string)


# @register.tag(name='date')
@register.tag
def date(parse, token):
    try:
        tagname, format_string = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('invalid args')
    return DateNode(eval(format_string))


# register.tag(name='date', compile_function=date)

@register.simple_tag
def get_current_time(format_string):
    return datetime.now().strftime(format_string)


@register.inclusion_tag('values.html')
def values(data_list, key):
    return {'data_list': data_list, 'key': key, 'hello': '<h1>hello</h1>'}


