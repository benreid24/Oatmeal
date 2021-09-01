import datetime
import time
import threading
import math
import statistics
import re

import smtplib
from email.message import EmailMessage

from . import secret

_thread = None
_heartbeat = None
TIMEOUT = datetime.timedelta(minutes=5)

MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)


def _verify():
    global _thread
    while True:
        if _heartbeat:
            if datetime.datetime.now() - _heartbeat >= TIMEOUT:
                _send_email(
                    'CRITICAL: Oatmeal Down',
                    'Heartbeat stopped from Oatmeal, check on Oatmeal ASAP'
                )
                break
        time.sleep(TIMEOUT.total_seconds()/2)
    _thread = None


def heartbeat():
    global _thread
    global _heartbeat

    _heartbeat = datetime.datetime.now()
    if not _thread:
        _thread = threading.Thread(target=_verify)
        _thread.start()


def is_mobile(request):
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def create_zones(temps, humidity):
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

    return zones, pairs


def compress_timeseries(data, pc):
    if len(data) < 2 * pc:
        return data

    inc = math.ceil(len(data) / pc)
    smdata = data[0::inc]
    smdata.append(data[-1])

    return smdata


def prepare_messages(messages, tz):
    classes = ['msgcrit', 'msgwarn', 'msginfo']

    return [{
        'class': classes[msg['level']-1],
        'msg': msg['msg'],
        'time': msg['time'].astimezone(tz).strftime('%a %b %d %I:%M %p')
    } for msg in messages]


def frequency_match_motion(motion, tz):
    now = datetime.datetime.now(datetime.timezone.utc)
    yday = now - datetime.timedelta(days=1)

    bucket_len = datetime.timedelta(seconds=300)

    buckets = []
    while yday < now:
        bucket = {
            'time': yday.astimezone(tz),
            'count': 0
        }
        buckets.append(bucket)
        yday = yday + bucket_len

    yday = now - datetime.timedelta(days=1)
    i = 0
    for dt in motion:
        if dt < yday or dt > now:
            continue
        while dt > buckets[i]['time'] + bucket_len:
            i += 1
        buckets[i]['count'] += 1

    total = sum([b['count'] for b in buckets])
    if total:
        buckets = [{
            'time': b['time'],
            'count': b['count'] / total * 10
        } for b in buckets]

    return buckets


def send_email(post):
    if not secret.valid_pw(post['pw']):
        return 'Invalid password'
    return _send_email(post['subject'], post['msg'])


def _send_email(subject, body):
    try:
        smtp = smtplib.SMTP('localhost')
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'him@oatmeal.rocks'
        msg['To'] = 'reidben24@gmail.com, anna.kasprzak@daemen.edu'
        msg.set_content(body)
        smtp.send_message(msg)
        smtp.quit()
    except Exception as err:
        return f'Error: {err}'
    return None
