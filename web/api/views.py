from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone

from . import db
from . import util

DESKTOP_PC = 900
MOBILE_PC = 100


def index(request):
    tzname = timezone('US/Eastern')

    pc = MOBILE_PC if util.is_mobile(request) else DESKTOP_PC
    temps = db.get_sensor_readings('temp', tzname, pc)
    humidity = db.get_sensor_readings('humid', tzname, pc)
    zones, pairs = util.create_zones(temps, humidity)

    messages = db.get_messages()
    messages = util.prepare_messages(messages, tzname)

    motion = db.get_motion()
    motion = util.frequency_match_motion(motion, tzname)

    context = {
        'pairs': pairs,
        'zones': zones,
        'messages': messages,
        'motion': motion,
        'video': db.get_video_url()
    }
    return render(request, 'app/index.html', context)


@csrf_exempt
def set_sensor(request):
    util.heartbeat()
    db.clean()
    error = db.set_reading(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)


@csrf_exempt
def add_info(request):
    util.heartbeat()
    db.clean()
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


@csrf_exempt
def send_mail(request):
    error = util.send_email(request.POST)
    if not error:
        return HttpResponse(status=204)
    return HttpResponse(error, status=400)
