from http import client as HttpClient
from urllib.parse import urlencode

import secret

ENDPOINT = 'oatmeal.rocks'

CRITICAL = 1
WARNING = 2
INFO = 3


def _send_request(url, params):
    params['pw'] = secret.get()
    params = urlencode(params)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        "Accept": 'text/plain'
    }
    client = HttpClient.HTTPConnection(ENDPOINT)
    client.request('POST', url, params, headers)
    return client.getresponse()


def set_sensor(name, reading, stype):
    params = {
        'name': name,
        'value': reading,
        'type': stype
    }
    response = _send_request('/setsensor', params)

    if response.status != 204:
        print('Sensor Error:', response.status, response.read())
        return False
    return True


def log_message(msg, severity):
    params = {
        'message': msg,
        'level': severity
    }
    response = _send_request('/addinfo', params)
    if response.status != 204:
        print('Log Error:', response.status, response.read())
        return False
    return True


def send_email(subject, msg):
    params = {
        'subject': subject,
        'msg': msg
    }
    response = _send_request('/sendmail', params)
    if response.status != 204:
        print('Email Error:', response.status, response.read())
        return False
    return True
