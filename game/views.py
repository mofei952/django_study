import json
import math
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from game import llk_service


def jigsaw(request):
    return render(request, 'jigsaw.html')


def llk(request):
    return render(request, 'llk.html')


@csrf_exempt
def llk_icon_map(request):
    data = request.POST
    icon_count = int(data.get('icon_count'))
    row_count = int(data.get('row_count'))
    col_count = int(data.get('col_count'))
    icon_map = llk_service.icon_map(icon_count, row_count, col_count)
    return HttpResponse(json.dumps(icon_map))


@csrf_exempt
def llk_connected(request):
    data = request.POST
    icon_map = json.loads(data.get('icon_map'))
    p1 = json.loads(data.get('p1'))
    p2 = json.loads(data.get('p2'))
    link_positions = llk_service.connected(icon_map, p1, p2)
    return HttpResponse(json.dumps(link_positions))


@csrf_exempt
def llk_status(request):
    data = request.POST
    icon_map = json.loads(data.get('icon_map'))
    status = llk_service.status(icon_map)
    return HttpResponse(json.dumps(status))


@csrf_exempt
def llk_hint(request):
    data = request.POST
    icon_map = json.loads(data.get('icon_map'))
    h = llk_service.hint(icon_map)
    return HttpResponse(json.dumps(h))
