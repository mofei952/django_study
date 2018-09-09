from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
from app1.models import Article


def articlelist(request):
    article_list = Article.objects.values('title', 'content', 'url', 'portal', 'author__name')
    print(article_list)
    article_list = Article.objects.all()
    return render(request, 'articlelist.html', {'article_list': article_list})


def addarticle(request):
    return render(request, 'addarticle.html')


def hello(request):
    return HttpResponse('<h1>helloworld</h1>')


def hello2(request, num):
    return HttpResponse('<h1>%s</h2' % num)


def test(request, id):
    print(request.path)
    return HttpResponse('<h1>%s</h1>' % id)


def test2(request, p, p2):
    return HttpResponse('<h1>%s,%s</h1>' % (p, p2))


def test3(request, page_number):
    return HttpResponse('<h1>%s</h1>' % page_number)


def page(request, num=1):
    raise Http404('111')
    return HttpResponse('<h1>%s,%s</h1>' % (num,str(type(num))))


def page_not_found(request, exception):
    return render(request, '404.html')