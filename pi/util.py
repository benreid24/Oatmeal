from urllib import request
import subprocess
import os
import smtplib
from email.message import EmailMessage

import secret

STREAM_URL = f'rtmp://a.rtmp.youtube.com/live2/{secret.stream_key()}'


def get_ip():
    return request.urlopen('https://api.ipify.org').read().decode('utf8')


def start_stream():
    null = open(os.devnull, 'w')
    process = subprocess.Popen(['bash', './startstream.sh', STREAM_URL], stderr=null, stdout=null)
    return process
