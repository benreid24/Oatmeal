import datetime

from .models import SensorReading
from .models import InfoMessage
from .models import VideoUrl

from . import secret


def _check_request(post):
    if not post:
        return 'Empty request'
    if not secret.valid_pw(post['pw']):
        return 'Authentication failed'
    return ''


def set_reading(post):
    err = _check_request(post)
    if err:
        return err
    try:
        obj = SensorReading()
        obj.name = post['name']
        obj.value = float(post['value'])
        obj.stype = post['type']
        SensorReading.save_model(obj)
    except Exception as exc:
        return repr(exc)


def add_info(post):
    err = _check_request(post)
    if err:
        return err
    try:
        obj = InfoMessage()
        obj.message = post['message']
        obj.level = int(post['level'])
        InfoMessage.save_model(obj)
    except Exception as exc:
        return repr(exc)


def set_url(post):
    err = _check_request(post)
    if err:
        return err
    try:
        obj = VideoUrl()
        obj.url = post['url']
        VideoUrl.objects.all().delete()
        obj.save()
    except Exception as exc:
        return repr(exc)


def get_sensor_readings(stype, tzname):
    now = datetime.datetime.now(datetime.timezone.utc)
    yday = now - datetime.timedelta(days=1)
    data = SensorReading.objects.filter(
        updated__range=(yday, now),
        stype=stype
    ).order_by('name', '-updated')
    output = {}
    for reading in data:
        if reading.name not in output.keys():
            output[reading.name] = {
                'value': reading.value,
                'updated': reading.updated.astimezone(tzname).strftime('%H:%M:%S (%b %d)'),
                'history': [{
                    'value': reading.value,
                    'time': reading.updated
                }]
            }
        else:
            output[reading.name]['history'].append({
                'value': reading.value,
                'time': reading.updated.astimezone(tzname)
            })

    output = [{
        'name': key,
        **value
    } for key, value in output.items()]
    return output
