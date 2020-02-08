from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from . import db


def index(request):
    tzname = request.session.get('django_timezone')
    context = {
        'temps': db.get_sensor_readings('temp', tzname)
    }
    return render(request, 'app/index.html', context)


@csrf_exempt
def set_sensor(request):
    error = db.set_reading(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)


@csrf_exempt
def add_info(request):
    error = db.add_info(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)


@csrf_exempt
def update_video(request):
    error = db.set_url(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)
