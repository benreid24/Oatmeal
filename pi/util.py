import subprocess
import os

import secret

STREAM_URL = f'rtmp://a.rtmp.youtube.com/live2/{secret.stream_key()}'


def start_stream():
    null = open(os.devnull, 'w')
    process = subprocess.Popen(['bash', './startstream.sh', STREAM_URL], stderr=null, stdout=null)
    return process
