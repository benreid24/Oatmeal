from urllib import request
import subprocess


def get_ip():
    return request.urlopen('https://api.ipify.org').read().decode('utf8')


def start_stream():
    subprocess.Popen(['./startstream.sh'], shell=True, executable='/bin/bash')
