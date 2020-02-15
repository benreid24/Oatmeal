from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from . import db


def index(request):
    tzname = request.session.get('django_timezone')
    temps = db.get_sensor_readings('temp', tzname)
    humidity = db.get_sensor_readings('humid', tzname)

    zones = []
    for name, temp in temps.items():
        if name not in humidity.keys():
            continue

        hhist = humidity[name]['history']
        fh = humidity[name]['history'][-1]['time']
        i = 0
        while i < len(temp['history']) and temp['history'][i]['time'] < fh:
            i += 1
        history = []
        for t in temp['history']:
            history.append({
                'time': t['time'],
                'temp': t['value'],
                'humid': hhist[i]['value'] if i < len(hhist) else hhist[-1]['value']
            })
            i += 1

        zones.append({
            'name': name if 'Zone' in name else f'{name} Zone',
            'temp': temp,
            'humid': humidity[name],
            'history': history
        })

    pairs = []
    pair = []
    for zone in zones:
        pair.append(zone)
        if len(pair) == 2:
            pairs.append(pair)
            pair = []
    if pair:
        pairs.append(pair)

    context = {
        'pairs': pairs,
        'zones': zones
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
