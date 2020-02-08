from django.shortcuts import render
from django.http import HttpResponse

from . import db


def index(request):
    return HttpResponse('This is where I will build the site')


def set_sensor(request):
    error = db.set_reading(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)


def add_info(request):
    error = db.add_info(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)


def update_video(request):
    error = db.set_url(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)
