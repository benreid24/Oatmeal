import datetime
import smtplib
from email.message import EmailMessage

from . import secret


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


def prepare_messages(messages, tz):
    classes = ['msgcrit', 'msgwarn', 'msginfo']

    return [{
        'class': classes[msg['level']-1],
        'msg': msg['msg'],
        'time': msg['time'].astimezone(tz).strftime('%a %b %d %I:%M %p')
    } for msg in messages]


def frequency_match_motion(motion, tz):
    if not motion:
        return []

    bucket_len = datetime.timedelta(seconds=300)
    bucket_beg = motion[0]

    buckets = []
    i = 0
    while i < len(motion):
        bucket = {
            'time': bucket_beg.astimezone(tz),
            'count': 0
        }
        while i < len(motion) and motion[i] < bucket_beg + bucket_len:
            bucket['count'] += 1
            i += 1
        buckets.append(bucket)
        bucket_beg += bucket_len

    return buckets


def send_email(post):
    if not secret.valid_pw(post['pw']):
        return 'Invalid password'

    try:
        smtp = smtplib.SMTP('localhost')
        msg = EmailMessage()
        msg['Subject'] = post['subject']
        msg['From'] = 'him@oatmeal.rocks'
        msg['To'] = 'reidben24@gmail.com, anna.kasprzak@daemen.edu'
        msg.set_content(post['msg'])
        smtp.send_message(msg)
        smtp.quit()
    except Exception as err:
        return f'Error: {err}'
    return None
