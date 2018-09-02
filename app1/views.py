from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from app1.models import Article


def hello(request):
    return HttpResponse('<h1>helloworld</h1>')


def hello2(request, num):
    return HttpResponse('<h1>%s</h2' % num)


def articlelist(request):
    article_list = Article.objects.all()
    return render(request, 'articlelist.html', {'article_list': article_list})
