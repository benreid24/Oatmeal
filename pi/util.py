from urllib import request
import subprocess
import smtplib
from email.message import EmailMessage


def get_ip():
    return request.urlopen('https://api.ipify.org').read().decode('utf8')


def start_stream():
    process = subprocess.Popen(['./startstream.sh'], shell=True, executable='/bin/bash')
    return process
